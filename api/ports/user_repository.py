from abc import ABC, abstractmethod

from api.models.user import User
from api.models.serializers.user import UserDTO


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserDTO) -> User: ...
