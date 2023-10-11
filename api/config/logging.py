from fastapi import Request, HTTPException
from starlette.concurrency import iterate_in_threadpool

from api.utils.logging import METHOD_MAPPING

from api.ports.user_log_repository import UserLogRepository

from api.models.user_log import UserLog, Area, Type

from datetime import datetime
import json
import jwt  # type:ignore


class Logging:

    def __init__(self, repository: UserLogRepository):
        self._repository = repository

    async def create_log_by_header(self, request: Request):
        authorization_header = request.headers.get("Authorization")
        if authorization_header:
            username = self._extract_username(authorization_header)
            user_log = self._create_user_log_from_header(request, username)

            if user_log:
                await self._repository.create_log(user_log)

    async def create_log_by_response_body(self, response, response_body_copy):
        response.body_iterator = iterate_in_threadpool(
            iter([response_body_copy]))
        response_data = json.loads(response_body_copy.decode())

        username = self._extract_username(
            "Bearer " + response_data.get("access_token"))
        user_log = UserLog(
            date=datetime.now(),
            user=username,
            area=Area.USUARIOS,
            type=Type.LOGIN,
            action=f"Registro de acesso do usuário {username} com sucesso"
        )

        await self._repository.create_log(user_log)

    def _create_user_log_from_header(self, request: Request, username: str) -> UserLog | None:
        full_url = str(request.url)

        if request.method in METHOD_MAPPING:
            type, area_mapping = METHOD_MAPPING[request.method]
            for area_name, area_mapped in area_mapping.items():
                if area_name in full_url:
                    area = area_mapped
                    action = f"Registro de {type.name.lower()} de {area.name.lower()} com sucesso"
                    break

        user_log = None
        if area and type and action:
            user_log = UserLog(
                date=datetime.now(),
                user=username,
                area=area,
                type=type,
                action=action
            )

        return user_log

    def _extract_username(self, authorization_header: str) -> str:
        token = self._retrieve_jwt(authorization_header)

        return self._retrieve_username(token)

    def _retrieve_jwt(self, authorization_header: str) -> str:
        auth_parts = authorization_header.split()
        if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
            raise HTTPException(401, "JWT inválido")

        return auth_parts[1]

    def _retrieve_username(self, token: str) -> str:
        try:
            payload = jwt.decode(token, algorithms=["HS256"], options={
                "verify_signature": False})
            username = payload.get("username")
        except jwt.DecodeError:
            raise HTTPException(401, "JWT inválido")

        return username
