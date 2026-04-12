from fastapi import FastAPI

from app.core.adapter import CollectorAdapter
from app.routes import create_router


def create_app() -> FastAPI:
    application = FastAPI()
    collector = CollectorAdapter()
    application.include_router(create_router(collector=collector))
    return application


app = create_app()
