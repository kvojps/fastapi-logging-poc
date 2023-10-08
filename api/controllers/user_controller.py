from fastapi import APIRouter, Depends, status

from api.adapters.user_adapter import UserAdapter
from api.models.serializers.user import UserDTO, UserResponse
from api.services.user_service import UserService

router = APIRouter()

adapter = UserAdapter()
service = UserService(adapter)


@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserDTO, user_service: UserService = Depends(lambda: service)):
    return user_service.create_user(user_data)
