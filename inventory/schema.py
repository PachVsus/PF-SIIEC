from datetime import datetime, timezone

from sqlalchemy import (
    Boolean, CheckConstraint, Column, DateTime, ForeignKey,
    Integer, MetaData, String, Table,
)

metadata = MetaData()
products = Table(
    "products", metadata,
    Column("id", Integer, primary_key=True),
    Column("sku", String(40), nullable=False, unique=True),
    Column("name", String(120), nullable=False),
    Column("stock", Integer, nullable=False, default=0),
    Column("active", Boolean, nullable=False, default=True),
    CheckConstraint("stock >= 0", name="stock_nonnegative"),
)
movements = Table(
    "movements", metadata,
    Column("id", Integer, primary_key=True),
    Column("product_id", ForeignKey("products.id"), nullable=False, index=True),
    Column("kind", String(10), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("note", String(200), nullable=False, default=""),
    Column("created_at", DateTime(timezone=True), nullable=False,
           default=lambda: datetime.now(timezone.utc)),
    CheckConstraint("quantity > 0", name="quantity_positive"),
    CheckConstraint("kind IN ('entrada', 'salida')", name="valid_kind"),
)
