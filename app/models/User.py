import time

from pydantic import BaseModel, EmailStr, HttpUrl


class User(BaseModel):
    id: int | None = int(time.time())
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl
