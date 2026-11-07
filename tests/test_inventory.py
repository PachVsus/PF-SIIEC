import os
import re
from concurrent.futures import ThreadPoolExecutor

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import insert, select

from inventory import create_app
from inventory.schema import metadata, movements, products
from inventory.service import record_movement


@pytest.fixture
def app(tmp_path, monkeypatch):
    # TEST_DATABASE_URL must point to a disposable database: tests reset tables.
    url = os.getenv("TEST_DATABASE_URL", "sqlite:///" + str(tmp_path / "test.db"))
    monkeypatch.setenv("DATABASE_URL", url)
    app = create_app({"TESTING": True, "DATABASE_URL": url,
                      "SECRET_KEY": "test-only", "WTF_CSRF_ENABLED": False})
    engine = app.extensions["db_engine"]
    command.upgrade(Config("alembic.ini"), "head")
    with engine.begin() as conn:
        conn.execute(movements.delete())
        conn.execute(products.delete())
    yield app
    engine.dispose()


@pytest.fixture
def engine(app):
    return app.extensions["db_engine"]


@pytest.fixture
def product(engine):
    with engine.begin() as conn:
        return conn.execute(insert(products).values(sku="SKU-001", name="Teclado")).inserted_primary_key[0]


def stock(engine, product):
    with engine.connect() as conn:
        return conn.scalar(select(products.c.stock).where(products.c.id == product))


def test_catalog_and_duplicate_code(app, engine):
    client = app.test_client()
    client.post("/products", data={"sku": "abc", "name": "Ratón"})
    response = client.post("/products", data={"sku": " ABC ", "name": "Otro"}, follow_redirects=True)
    assert "Ya existe" in response.text
    with engine.connect() as conn:
        assert len(conn.execute(select(products)).all()) == 1
    assert "Ratón" in client.get("/?q=rat").text
    assert "No hay coincidencias" in client.get("/?q=ausente").text


def test_valid_movements_and_history(app, engine, product):
    client = app.test_client()
    for kind, quantity in [("entrada", 10), ("salida", 4)]:
        response = client.post(f"/products/{product}/movements", data={
            "kind": kind, "quantity": quantity, "note": "Prueba"
        }, follow_redirects=True)
        assert "Movimiento registrado" in response.text
    assert stock(engine, product) == 6
    with engine.connect() as conn:
        assert len(conn.execute(select(movements)).all()) == 2


@pytest.mark.parametrize("kind,quantity", [
    ("salida", "1"), ("entrada", "0"), ("salida", "-1"),
    ("entrada", "1.5"), ("entrada", "texto"), ("otro", "1"),
    ("entrada", "2147483648"),
])
def test_invalid_movement_leaves_no_changes(engine, product, kind, quantity):
    with pytest.raises(ValueError):
        record_movement(engine, product, kind, quantity)
    assert stock(engine, product) == 0
    with engine.connect() as conn:
        assert conn.execute(select(movements)).first() is None


def test_deactivate_preserves_history(app, engine, product):
    record_movement(engine, product, "entrada", "5")
    client = app.test_client()
    client.post(f"/products/{product}", data={"name": "Teclado nuevo"})
    with pytest.raises(ValueError):
        record_movement(engine, product, "salida", "1")
    assert stock(engine, product) == 5
    assert "Teclado nuevo" in client.get(f"/products/{product}").text
    client.post(f"/products/{product}", data={"name": "Teclado", "active": "on"})
    record_movement(engine, product, "salida", "1")
    assert stock(engine, product) == 4


def test_concurrent_withdrawals_never_make_negative_stock(engine, product):
    record_movement(engine, product, "entrada", "5")

    def withdraw(_):
        try:
            record_movement(engine, product, "salida", "4")
            return True
        except ValueError:
            return False

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(withdraw, range(2)))
    assert sum(results) == 1
    assert stock(engine, product) == 1


def test_persistence_across_app_restart(app, engine, product):
    record_movement(engine, product, "entrada", "7")
    second = create_app({"TESTING": True, "DATABASE_URL": app.config["DATABASE_URL"]})
    try:
        assert stock(second.extensions["db_engine"], product) == 7
        assert second.test_client().get("/health").json["status"] == "ok"
    finally:
        second.extensions["db_engine"].dispose()


def test_csrf_and_missing_product(app):
    app.config["WTF_CSRF_ENABLED"] = True
    client = app.test_client()
    assert client.post("/products", data={"sku": "X", "name": "X"}).status_code == 400
    assert client.get("/products/99999").status_code == 404


def test_form_with_real_csrf_token(app):
    app.config["WTF_CSRF_ENABLED"] = True
    client = app.test_client()
    token = re.search(r'name="csrf_token" value="([^"]+)"', client.get("/").text).group(1)
    response = client.post("/products", data={
        "sku": "CSRF-OK", "name": "Producto de prueba", "csrf_token": token
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Producto registrado" in response.text


def test_health_reports_uninitialized_database(tmp_path):
    uninitialized = create_app({"DATABASE_URL": "sqlite:///" + str(tmp_path / "empty.db")})
    assert uninitialized.test_client().get("/health").status_code == 503
    uninitialized.extensions["db_engine"].dispose()
