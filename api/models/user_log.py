from datetime import datetime
from enum import Enum
from beanie import Document


class Type(Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    EDICAO = "EDICAO"
    CRIACAO = "CRIACAO"
    EXCLUSAO = "EXCLUSAO"


class UserLog(Document):
    date: datetime
    user: str
    type: Type
    action: str
