import motor.motor_asyncio

from beanie import init_beanie

from api.config.dynaconf import settings


async def init_mongo_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DB_URI)
    await init_beanie(database=client['logging'], document_models=['api.models.user_log.UserLog'])
