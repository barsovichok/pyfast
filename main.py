import json

from fastapi import FastAPI

from support_data import SupportData
from user_data import UserData, NewUser
from user_response import UserResponse

app = FastAPI()


def get_data():
    with open('default_user.json') as file_data:
        return json.load(file_data)


@app.get("/")
def read_root():
    return "Hey! It's Tatiana's first fastapi microservice!"


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user_data = get_data()
    user_data["id"] = user_id
    support_data = SupportData(
        url="https://reqres.in/#support-heading",
        text="To keep ReqRes free, contributions towards server costs are appreciated!"
    )

    response = UserResponse(data=user_data, support=support_data)
    return response


@app.post("/api/users/", response_model=UserResponse)
def create_user(user: NewUser):
    user_data = UserData(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        avatar=user.avatar,
    )

    support_data = SupportData(
        url="https://reqres.in/#support-heading",
        text="To keep ReqRes free, contributions towards server costs are appreciated!"
    )
    response = UserResponse(data=user_data, support=support_data)
    return response


@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user(user: NewUser, user_id: int):
    user_data = UserData(
        id=user_id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        avatar=user.avatar,
    )

    support_data = SupportData(
        url="https://reqres.in/#support-heading",
        text="To keep ReqRes free, contributions towards server costs are appreciated!"
    )
    response = UserResponse(data=user_data, support=support_data)
    return response
