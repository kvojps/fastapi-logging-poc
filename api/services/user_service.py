from fastapi import HTTPException, status

from api.config.security import get_hashed_password, verify_password, create_access_token, create_refresh_token

from api.ports.user_repository import UserRepository

from api.models.user import User
from api.models.serializers.user import UserDTO, UserResponse
from api.models.serializers.auth import AuthResponse


class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def login_user(self, user_data: UserDTO) -> AuthResponse:
        user: User = self._user_repo.get_user_by_email(user_data.email)
        hashed_password = str(user.password)
        email = str(user.email)

        if not verify_password(user_data.password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )

        return AuthResponse(
            access_token=create_access_token(email, None),
            refresh_token=create_refresh_token(email, None)
        )

    def create_user(self, user_data: UserDTO) -> UserResponse:
        hashed_password = get_hashed_password(user_data.password)
        user_data.password = hashed_password
        user: User = self._user_repo.create_user(user_data)

        return UserResponse(id=int(user.id), email=str(user.email))

    def get_users(self) -> list[UserResponse]:
        users: list[User] = self._user_repo.get_users()
        users_response = [UserResponse(
            id=int(user.id), email=str(user.email)) for user in users]

        return users_response

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user: User = self._user_repo.get_user_by_id(user_id)
        return UserResponse(id=int(user.id), email=str(user.email))

    def get_user_by_email(self, email: str) -> UserResponse:
        user: User = self._user_repo.get_user_by_email(email)
        return UserResponse(id=int(user.id), email=str(user.email))
