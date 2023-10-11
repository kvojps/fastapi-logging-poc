from .user import User
from api.config.postgres_db import engine


def create_tables():
    user.Base.metadata.create_all(bind=engine)
