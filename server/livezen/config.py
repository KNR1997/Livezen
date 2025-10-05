import os
import logging
from dotenv import load_dotenv

from starlette.config import Config

log = logging.getLogger(__name__)


load_dotenv()

# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))


TORTOISE_ORM = {
    "connections": {
        # SQLite configuration
        "sqlite": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": f"{BASE_DIR}/db.sqlite3"},  # Path to SQLite database file
        },
        # "default": f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    },
    "apps": {
        "models": {
            # include all your domain model modules
            "models": [
                "livezen.auth.models",
                "livezen.type.models",
                "livezen.category.models",
                "livezen.product.models",
                "livezen.tag.models",
                "livezen.wishlist.models",
                "aerich.models"  # 👈 Aerich needs this
            ],
            "default_connection": "sqlite",
        },
    },
}

config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
YMA_JWT_SECRET = config("YMA_JWT_SECRET", default="secret-key")
YMA_JWT_ALG = config("YMA_JWT_ALG", default="HS256")
YMA_JWT_EXP = config("YMA_JWT_EXP", cast=int, default=86400)  # Seconds
