from fastapi import APIRouter

from .health_check import router as health_check_router
from .user_controller import router as user_router

main_router = APIRouter()

main_router.include_router(health_check_router, prefix="/health_check", tags=['Health check'])
main_router.include_router(user_router, prefix="/users", tags=['User'])
