from .user import User
from api.config.db import engine


def create_tables():
    user.Base.metadata.create_all(bind=engine)
