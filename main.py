from fastapi import FastAPI

from app.routes import create_router


def create_app() -> FastAPI:
    application = FastAPI()
    application.include_router(create_router())
    return application


app = create_app()
