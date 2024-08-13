import os
import dotenv
import pytest

from app.routers.users import get_count_users


@pytest.fixture(autouse=True, scope="session")
def env():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv('APP_URL')


@pytest.fixture(scope="module")
def total_users() -> int:
    return get_count_users()



@pytest.fixture()
def pagination(total_users, size):
    if total_users % size == 0:
        return total_users // size
    else:
        return total_users // size + 1
