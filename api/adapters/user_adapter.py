from api.models.user import User
from api.models.serializers.user import UserDTO
from api.ports.user_repository import UserRepository
from api.config.db import SessionLocal


class UserAdapter(UserRepository):
    def __init__(self):
        self._session = SessionLocal()

    def create_user(self, user: UserDTO) -> User:
        user_data = User(email=user.email, password=user.password)
        self._session.add(user_data)
        self._session.commit()
        self._session.refresh(user_data)
        return user_data
