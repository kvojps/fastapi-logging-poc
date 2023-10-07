from fastapi import FastAPI

from api.controller import main_router

app = FastAPI(
    title="API - Aluguel de imóveis",
    version="0.1.0",
    description="API Rest para sistema de aluguel de imóveis"
)

app.include_router(main_router)
