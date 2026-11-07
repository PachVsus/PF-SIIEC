from sqlalchemy import insert, update

from .schema import movements, products


def text_field(value, label, limit):
    value = str(value or "").strip()
    if not value or len(value) > limit:
        raise ValueError(f"{label}: usa entre 1 y {limit} caracteres.")
    return value


def record_movement(engine, product_id, kind, quantity, note=""):
    if kind not in ("entrada", "salida"):
        raise ValueError("Tipo de movimiento inválido.")
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        raise ValueError("La cantidad debe ser un entero positivo.") from None
    if quantity <= 0 or quantity > 2_147_483_647:
        raise ValueError("La cantidad debe ser un entero positivo válido.")
    note = str(note).strip()
    if len(note) > 200:
        raise ValueError("La nota no puede superar 200 caracteres.")
    # Actualización condicional atómica: dos salidas concurrentes no pueden
    # consumir las mismas existencias. Stock e historial comparten transacción.
    with engine.begin() as conn:
        stmt = update(products).where(
            products.c.id == product_id, products.c.active.is_(True)
        )
        if kind == "salida":
            stmt = stmt.where(products.c.stock >= quantity)
            new_stock = products.c.stock - quantity
        else:
            stmt = stmt.where(products.c.stock <= 2_147_483_647 - quantity)
            new_stock = products.c.stock + quantity
        result = conn.execute(stmt.values(stock=new_stock))
        if result.rowcount != 1:
            raise ValueError("Movimiento rechazado: verifica producto activo, cantidad y existencias.")
        conn.execute(insert(movements).values(
            product_id=product_id, kind=kind, quantity=quantity, note=note
        ))
