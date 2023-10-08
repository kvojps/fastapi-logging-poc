from fastapi import APIRouter, Depends, status

from api.adapters.user_adapter import UserAdapter
from api.models.serializers.user import UserDTO
from api.models.serializers.auth import AuthResponse
from api.services.user_service import UserService

router = APIRouter()

adapter = UserAdapter()
service = UserService(adapter)


@router.post('/login', response_model=AuthResponse, status_code=status.HTTP_200_OK)
def login_user(user_data: UserDTO, user_service: UserService = Depends(lambda: service)):
    return user_service.login_user(user_data)
