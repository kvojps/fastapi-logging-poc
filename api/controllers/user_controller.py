from fastapi import APIRouter, Depends, status

from api.security import AuthenticatedUser

from api.services.user_service import UserService

from api.adapters.user_adapter import UserAdapter

from api.models.serializers.user import UserDTO, UserResponse


router = APIRouter()

adapter = UserAdapter()
service = UserService(adapter)


@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserDTO, user_service: UserService = Depends(lambda: service)):
    return user_service.create_user(user_data)


@router.get('', dependencies=[Depends(AuthenticatedUser)], response_model=list[UserResponse],
            status_code=status.HTTP_200_OK)
def get_users(user_service: UserService = Depends(lambda: service)):
    return user_service.get_users()


@router.get('/{user_id}', dependencies=[Depends(AuthenticatedUser)], response_model=UserResponse,
            status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, user_service: UserService = Depends(lambda: service)):
    return user_service.get_user_by_id(user_id)
