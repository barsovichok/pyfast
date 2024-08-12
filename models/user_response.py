from pydantic import BaseModel
from models.User import User
from models.support_data import SupportData


class UserResponse(BaseModel):
    data: User
    support: SupportData

