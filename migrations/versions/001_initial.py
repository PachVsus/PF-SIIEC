"""Create product catalog and movement ledger."""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "products", sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sku", sa.String(40), nullable=False, unique=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.CheckConstraint("stock >= 0", name="stock_nonnegative"),
    )
    op.create_table(
        "movements", sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("kind", sa.String(10), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("note", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("quantity > 0", name="quantity_positive"),
        sa.CheckConstraint("kind IN ('entrada', 'salida')", name="valid_kind"),
    )
    op.create_index("ix_movements_product_id", "movements", ["product_id"])


def downgrade():
    op.drop_table("movements")
    op.drop_table("products")
