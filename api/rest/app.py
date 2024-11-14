from importlib import import_module

from fastapi import FastAPI
from rest.extensions import config


def create_app() -> FastAPI:
    app = FastAPI(root_path=config.APPLICATION_ROOT)
    init_routes(app)
    return app


def init_routes(app: FastAPI) -> None:
    for route in config.ROUTES:
        module = import_module(route)
        app.include_router(module.router)
