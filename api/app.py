import asyncio

from fastapi import FastAPI, Request

from api.config.postgres_db import init_postgres_db
from api.config.mongo_db import init_mongo_db
from api.config.logging import Logging

from api.controllers import main_router

from api.adapters.user_log_adapter import UserLogAdapter

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


@app.middleware("http")
async def logging(request: Request, call_next):
    response = await call_next(request)

    if request.method == "GET":
        return response

    base_url = str(request.base_url)
    full_url = str(request.url)
    signin_url = f'{base_url}auth/login'

    if 200 <= response.status_code < 300:
        repository = UserLogAdapter()
        logging = Logging(repository)
        loop = asyncio.get_event_loop()
        authorization_header = request.headers.get("Authorization")

        if full_url == signin_url:
            response_body_copy = b''.join([chunk async for chunk in response.body_iterator])
            loop.create_task(logging.create_log_by_response_body(
                response, response_body_copy))
        elif authorization_header:
            loop.create_task(logging.create_log_by_header(request))

    return response


app.include_router(main_router)
