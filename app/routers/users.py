from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate

from database import users_db
from models.User import User

router = APIRouter(prefix="/api/users")


@router.get("/", status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    return paginate(users_db)


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive integer")
    if user_id not in range(len(users_db)):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users_db[user_id - 1]
