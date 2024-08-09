import time

from pydantic import BaseModel


class NewUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    avatar: str


class UserData(BaseModel):
    id: int | None = int(time.time())
    email: str
    first_name: str
    last_name: str
    avatar: str
