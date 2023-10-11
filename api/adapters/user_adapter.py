from api.config.postgres_db import SessionLocal

from api.ports.user_repository import UserRepository

from api.models.user import User
from api.models.serializers.user import UserDTO


class UserAdapter(UserRepository):

    def __init__(self):
        self._session = SessionLocal()

    def create_user(self, user: UserDTO) -> User:
        user_data = User(email=user.email, password=user.password)
        self._session.add(user_data)
        self._session.commit()
        self._session.refresh(user_data)
        return user_data

    def get_users(self) -> list[User]:
        return self._session.query(User).all()

    def get_user_by_id(self, user_id: int) -> User:
        return self._session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:
        return self._session.query(User).filter(User.email == email).first()
