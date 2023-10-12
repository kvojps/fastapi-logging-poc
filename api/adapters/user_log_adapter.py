from datetime import datetime
from math import ceil
from typing import Optional

from api.models.user_log import Area, Type, UserLog
from api.ports.user_log_repository import UserLogRepository
from beanie.operators import GTE, LTE, RegEx
from beanie.odm.enums import SortDirection


class UserLogAdapter(UserLogRepository):

    _user_log_model = UserLog

    async def create_log(self, log_data: UserLog):
        return await self._user_log_model.create(log_data)

    async def get_log(self, initial_date: Optional[datetime],
                      final_date: Optional[datetime], area: Optional[Area], type: Optional[Type],
                      user: Optional[str], action: Optional[str], is_ordered: Optional[bool] = False,
                      logs_per_page: int = 20, page: int = 1) -> dict:

        if logs_per_page <= 0 or page <= 0:
            raise Exception("Please, verify logs per page or page filter.")

        filters = [
            GTE(self._user_log_model.date,
                initial_date) if initial_date is not None else None,
            LTE(self._user_log_model.date,
                final_date) if final_date is not None else None,
            self._user_log_model.area == area if area is not None else None,
            self._user_log_model.type == type if type is not None else None,
            self._user_log_model.user == user if user is not None else None,
            RegEx(self._user_log_model.action,
                  action) if action is not None else None
        ]

        filtered_filters = [f for f in filters if f is not None]

        logs = []

        if is_ordered:
            logs = await self._user_log_model.find(*filtered_filters, sort=[("date", SortDirection.DESCENDING)]).skip(logs_per_page * (page - 1)).limit(logs_per_page).to_list()
        else:
            logs = await self._user_log_model.find(*filtered_filters).skip(logs_per_page * (page - 1)).limit(logs_per_page).to_list()

        all_logs = await self._user_log_model.find(*filtered_filters).to_list()
        total_pages = ceil(len(all_logs) / logs_per_page)

        result = {
            "logs": logs,
            "total_logs": len(all_logs),
            "logs_per_page": logs_per_page,
            "current_page": page,
            "total_pages": total_pages
        }

        return result

    async def get_log_by_id(self, log_id: str):
        return self._user_log_model.find_one({"_id": log_id})
