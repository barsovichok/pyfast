import time

from pydantic import BaseModel


class NewUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    avatar: str


class UserData(BaseModel):
    id: int | None = str(int(time.time()))
    email: str
    first_name: str
    last_name: str
    avatar: str


default_user_data = UserData(
    email="janet.weaver@reqres.in",
    first_name="Janet",
    last_name="Weaver",
    avatar="https://reqres.in/img/faces/2-image.jpg"
)
