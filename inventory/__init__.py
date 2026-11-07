import os
import secrets
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine, event, func, insert, select, text, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .schema import movements, products
from .service import record_movement, text_field


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY") or secrets.token_hex(32),
        DATABASE_URL=os.getenv("DATABASE_URL") or
        "sqlite:///" + str(Path(app.instance_path) / "inventory.db"),
        MAX_CONTENT_LENGTH=16 * 1024,
        SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
        APP_VERSION=os.getenv("APP_VERSION", "local"),
    )
    if config:
        app.config.update(config)
    CSRFProtect(app)
    engine = create_engine(app.config["DATABASE_URL"], pool_pre_ping=True)
    if engine.dialect.name == "sqlite":
        @event.listens_for(engine, "connect")
        def configure_sqlite(conn, _):
            conn.execute("PRAGMA foreign_keys=ON")
    app.extensions["db_engine"] = engine

    @app.after_request
    def headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'"
        )
        return response

    @app.get("/health")
    def health():
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.execute(select(products.c.id).limit(1))
            return {"status": "ok", "version": app.config["APP_VERSION"]}
        except SQLAlchemyError:
            app.logger.exception("Health check failed")
            return {"status": "unavailable"}, 503

    @app.get("/")
    def index():
        query = request.args.get("q", "").strip()[:120]
        stmt = select(products).order_by(products.c.id)
        if query:
            pattern = "%" + query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
            stmt = stmt.where(products.c.name.ilike(pattern, escape="\\") |
                              products.c.sku.ilike(pattern, escape="\\"))
        with engine.connect() as conn:
            rows = conn.execute(stmt).mappings().all()
            totals = conn.execute(select(
                func.count(products.c.id), func.coalesce(func.sum(products.c.stock), 0)
            )).one()
        return render_template("index.html", products=rows, totals=totals, query=query)

    @app.post("/products")
    def create_product():
        try:
            sku = text_field(request.form.get("sku"), "Código", 40).upper()
            name = text_field(request.form.get("name"), "Nombre", 120)
            with engine.begin() as conn:
                conn.execute(insert(products).values(sku=sku, name=name))
            flash("Producto registrado. Agrega existencias con una entrada.", "success")
        except ValueError as exc:
            flash(str(exc), "error")
        except IntegrityError:
            flash("Ya existe un producto con ese código.", "error")
        return redirect(url_for("index"))

    @app.route("/products/<int:product_id>", methods=["GET", "POST"])
    def product_detail(product_id):
        if request.method == "POST":
            try:
                name = text_field(request.form.get("name"), "Nombre", 120)
                with engine.begin() as conn:
                    result = conn.execute(update(products).where(products.c.id == product_id).values(
                        name=name, active=request.form.get("active") == "on"
                    ))
                    if result.rowcount != 1:
                        abort(404)
                flash("Producto actualizado.", "success")
            except ValueError as exc:
                flash(str(exc), "error")
            return redirect(url_for("product_detail", product_id=product_id))
        with engine.connect() as conn:
            product = conn.execute(select(products).where(products.c.id == product_id)).mappings().first()
            if not product:
                abort(404)
            history = conn.execute(select(movements).where(
                movements.c.product_id == product_id
            ).order_by(movements.c.id.desc())).mappings().all()
        return render_template("product.html", product=product, history=history)

    @app.post("/products/<int:product_id>/movements")
    def movement(product_id):
        try:
            record_movement(engine, product_id, request.form.get("kind"),
                            request.form.get("quantity"), request.form.get("note", ""))
            flash("Movimiento registrado.", "success")
        except ValueError as exc:
            flash(str(exc), "error")
        return redirect(url_for("product_detail", product_id=product_id))

    return app
