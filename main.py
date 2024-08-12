import json
from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, add_pagination, paginate

from models.AppStatus import AppStatus
from models.User import User


app = FastAPI()
add_pagination(app)

with open('users.json') as file_data:
    users = json.load(file_data)
    for user in users:
        User.model_validate(user)


@app.get("/status", status_code=HTTPStatus.OK)
def check_status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.get("/api/users", status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    return paginate(users)


@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive integer")
    if user_id not in range(len(users)):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@app.post("/api/users/", response_model=User, status_code=201)
def create_user(user: User):
    user_data = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        avatar=user.avatar,
    )

    return user_data


@app.put("/api/users/{user_id}", response_model=User)
def update_user(user: User, user_id: int):
    user_data = User(
        id=user_id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        avatar=user.avatar,
    )
    return user_data


@app.delete("/api/users/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    return None
