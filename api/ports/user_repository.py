from abc import ABC, abstractmethod

from api.models.user import User
from api.models.serializers.user import UserDTO


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserDTO) -> User: ...

    @abstractmethod
    def get_users(self) -> list[User]: ...

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User: ...

    @abstractmethod
    def get_user_by_email(self, email: str) -> User: ...
