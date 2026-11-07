"""Start the local demonstration with migrations and a production WSGI server."""
from pathlib import Path
from dotenv import load_dotenv
from alembic import command
from alembic.config import Config
from waitress import serve
from inventory import create_app

if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    load_dotenv(root / ".env")
    config = Config(str(root / "alembic.ini"))
    config.set_main_option("script_location", str(root / "migrations"))
    command.upgrade(config, "head")
    print("Inventario disponible en http://127.0.0.1:8000", flush=True)
    serve(create_app(), host="127.0.0.1", port=8000)
