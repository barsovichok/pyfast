import os
import dotenv
import pytest


@pytest.fixture(autouse=True)
def env():
    dotenv.load_dotenv()


@pytest.fixture()
def app_url():
    return os.getenv('APP_URL')


@pytest.fixture()
def total(users):
    return len(users)
@pytest.fixture()
def pagination(total, size):
    if total % size == 0:
        return total // size
    else:
        return total // size + 1
