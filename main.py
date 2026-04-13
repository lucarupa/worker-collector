import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapter import CollectorAdapter
from app.routes import create_router
from app.services.kafka.consumer import start_kafka_consumer


def create_app() -> FastAPI:
    collector = CollectorAdapter()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        task = asyncio.create_task(start_kafka_consumer(collector))
        yield
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    application = FastAPI(lifespan=lifespan)
    application.include_router(create_router(collector=collector))
    return application


app = create_app()
