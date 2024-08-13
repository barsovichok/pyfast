from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate

from app.database import users
from app.models.User import User, UserCreate, UserUpdate

router = APIRouter(prefix="/api/users")


@router.get("/count", status_code=HTTPStatus.OK)
def get_count_users() -> int:
    return users.get_count_users()


@router.get("/", status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    return paginate(users.get_users())


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive integer")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: User) -> User:
    UserCreate.model_validate(user.model_dump())
    return users.create_user(user)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: User):
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive integer")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive integer")
    if not users.delete_user(user_id):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    users.delete_user(user_id)
    return {"message": "User deleted successfully"}
