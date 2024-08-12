from http import HTTPStatus

from fastapi import APIRouter

from app.database import users_db
from app.models.AppStatus import AppStatus

router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def check_status() -> AppStatus:
    return AppStatus(users=bool(users_db))
