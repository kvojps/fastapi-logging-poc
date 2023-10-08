from pydantic import BaseModel


class UserDTO(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
