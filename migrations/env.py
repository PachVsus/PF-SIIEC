import os
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine
from inventory.schema import metadata

url = os.environ.get("DATABASE_URL") or "sqlite:///" + str(
    Path(__file__).resolve().parents[1] / "instance" / "inventory.db"
)
Path("instance").mkdir(exist_ok=True)
if context.is_offline_mode():
    context.configure(url=url, target_metadata=metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    engine = create_engine(url)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=metadata)
        with context.begin_transaction():
            context.run_migrations()
