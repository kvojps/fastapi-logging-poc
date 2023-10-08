from fastapi import APIRouter, Depends

from .health_check import router as health_check_router
from .user_controller import router as user_router
from .auth_controller import router as auth_router
from api.security import AuthenticatedUser

main_router = APIRouter()

main_router.include_router(health_check_router, prefix="/health_check", tags=['Health check'],
                           dependencies=[Depends(AuthenticatedUser)])
main_router.include_router(user_router, prefix="/users", tags=['User'])
main_router.include_router(auth_router, prefix="/auth", tags=['Auth'])
