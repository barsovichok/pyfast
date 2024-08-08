import time
from pydantic import BaseModel
from user_data import UserData, NewUser
from support_data import SupportData


class UserResponse(BaseModel):
    data: UserData
    support: SupportData


class CreateUserResponse(BaseModel):
    data: NewUser
    support: SupportData
