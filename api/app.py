from fastapi import FastAPI

from api.config.db import init_db

from api.controllers import main_router

from api.models import create_tables

app = FastAPI(
    title="API - Aluguel de imóveis",
    version="0.1.0",
    description="API Rest para sistema de aluguel de imóveis"
)


@app.on_event("startup")
def start_db():
    create_tables()
    init_db()


app.include_router(main_router)
