from fastapi import HTTPException
from typing import Sequence, Type
from sqlalchemy import table, column

from .engine import engine
from sqlmodel import Session, select, func

from ..models.User import User


def get_user(user_id: int) -> User | None:
    with Session(engine) as session:
        return session.get(User, user_id)


def get_users() -> Sequence[User] | None:
    with Session(engine) as session:
        return session.exec(select(User)).all()


def get_count_users() -> int:
    with Session(engine) as session:
        users_column = table('user', column('id'))
        statement = select(func.count()).select_from(users_column)
        return session.execute(statement).scalar()


def create_user(user: User) -> User:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)  # Refresh the object to get the generated ID.
        return user


def delete_user(user_id: int) -> bool:
    try:
        with Session(engine) as session:
            user = session.get(User, user_id)
            session.delete(user)
            session.commit()
            return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False


def update_user(user_id: int, user: User) -> HTTPException | Type[User]:
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            return HTTPException(status_code=404, detail="User not found")
        user_data = db_user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
