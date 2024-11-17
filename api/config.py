import os

from alembic.config import Config
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class AppConfig:
    ROUTES = [
        "rest.views.tag",
        "rest.views.timer",
    ]
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('SQLALCHEMY_DATABASE_URI', "")
    SQLALCHEMY_DATABASE_URI_ALEMBIC: str = os.environ.get('SQLALCHEMY_DATABASE_URI_ALEMBIC', "")
    SQLALCHEMY_DATABASE_URI_TEST: str = os.environ.get('SQLALCHEMY_DATABASE_URI_TEST', "")
    SQLALCHEMY_DATABASE_URI_TEST_ALEMBIC: str = os.environ.get('SQLALCHEMY_DATABASE_URI_TEST_ALEMBIC', "")
    APPLICATION_ROOT: str = "/api/v1"


alembic_cfg = Config('alembic.ini')
