from api.models.user import User
from api.models.serializers.user import UserDTO, UserResponse
from api.ports.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def create_user(self, user_data: UserDTO) -> UserResponse:
        user: User = self._user_repo.create_user(user_data)
        return UserResponse(id=user.id, email=user.email)
