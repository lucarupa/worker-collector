import asyncio
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from injector import Injector

from app.adapter import CollectorAdapter
from app.core.env.mongo_env import MongoEnv
from app.routes import create_router
from app.services.database_injection import DatabaseModule
from app.services.kafka.consumer import start_kafka_consumer

load_dotenv()


def create_app() -> FastAPI:
    mongo_env = MongoEnv().search_environment_variables()

    injector: Injector = Injector(
        [
            DatabaseModule(
                connection_string=mongo_env.connection_string,
                database=mongo_env.database,
            )
        ]
    )

    collector = CollectorAdapter(injector=injector)

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
