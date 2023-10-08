from api.models.user import User
from api.models.serializers.user import UserDTO, UserResponse
from api.ports.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def create_user(self, user_data: UserDTO) -> UserResponse:
        user: User = self._user_repo.create_user(user_data)
        return UserResponse(id=user.id, email=user.email)

    def get_users(self) -> list[UserResponse]:
        users: list[User] = self._user_repo.get_users()
        users_response = [UserResponse(id=user.id, email=user.email) for user in users]

        return users_response

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user: User = self._user_repo.get_user_by_id(user_id)
        return UserResponse(id=user.id, email=user.email)

    def get_user_by_email(self, email: str) -> UserResponse:
        user: User = self._user_repo.get_user_by_email(email)
        return UserResponse(id=user.id, email=user.email)
