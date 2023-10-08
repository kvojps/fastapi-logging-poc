from fastapi import FastAPI

from api.controller import main_router
from api.models import user
from api.config.db import init_db, engine

app = FastAPI(
    title="API - Aluguel de imóveis",
    version="0.1.0",
    description="API Rest para sistema de aluguel de imóveis"
)


@app.on_event("startup")
def start_db():
    # refatorar apos criacao de repositorios
    user.Base.metadata.create_all(bind=engine)
    init_db()


app.include_router(main_router)
