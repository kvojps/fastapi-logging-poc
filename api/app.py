from fastapi import FastAPI

from api.config.postgres_db import init_postgres_db
from api.config.mongo_db import init_mongo_db

from api.controllers import main_router

from api.models import create_tables

app = FastAPI(
    title="API - Aluguel de imóveis",
    version="0.1.0",
    description="API Rest para sistema de aluguel de imóveis"
)


@app.on_event("startup")
def start_postgres_db():
    create_tables()
    init_postgres_db()


@app.on_event("startup")
async def start_mongo_db():
    await init_mongo_db()


app.include_router(main_router)
