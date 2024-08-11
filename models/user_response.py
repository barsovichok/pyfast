from pydantic import BaseModel
from models.user_data import UserData, NewUser
from models.support_data import SupportData


class UserResponse(BaseModel):
    data: UserData
    support: SupportData


class CreateUserResponse(BaseModel):
    data: NewUser
    support: SupportData
