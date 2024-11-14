import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class Config:
    ROUTES = [
        "rest.views.tag",
        "rest.views.timer",
    ]
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('SQLALCHEMY_DATABASE_URI', "")
    SQLALCHEMY_DATABASE_URI_ALEMBIC: str = os.environ.get('SQLALCHEMY_DATABASE_URI_ALEMBIC', "")
