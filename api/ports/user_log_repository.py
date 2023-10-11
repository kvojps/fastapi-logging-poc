from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from api.models.user_log import UserLog


class UserLogRepository(ABC):

    @abstractmethod
    async def create_log(self, log_data: UserLog): ...
