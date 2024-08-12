import json
import uvicorn
from http import HTTPStatus
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from database import users_db
from routers import status, users
from models.User import User

app = FastAPI()

app.include_router(status.router)
app.include_router(users.router)

add_pagination(app)



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


if __name__ == "__main__":

    with open('../users.json') as file_data:
        users_db.extend(json.load(file_data))
        for user in users_db:
            User.model_validate(user)
    uvicorn.run(app, host="0.0.0.0", port=8000)