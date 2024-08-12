import json
from http import HTTPStatus
import pytest
from models.User import User
import requests


payload = {
    "email": "3242@gmail.com",
    "first_name": "FirstName",
    "last_name": "LastName",
    "avatar": "https://reqres.in/png/faces/1383-image.jpg"
}


@pytest.fixture()
def users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    users = response.json().get("items")
    for user in users:
        User.model_validate(user)
    return users


def test_users_no_doubles(users):
    user_ids = [user["id"] for user in users]
    assert len(user_ids) == len(set(user_ids))


def test_post_method(app_url):
    response = requests.post(f"{app_url}/api/users/", data=json.dumps(payload))
    assert response.status_code == 201
    User.model_validate(response.json())


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_put_method(app_url, user_id):
    response = requests.put(f"{app_url}/api/users/{user_id}", data=json.dumps(payload))
    assert response.status_code == HTTPStatus.OK
    User.model_validate(response.json())


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_get_method(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    User.model_validate(response.json())


def test_get_method_not_allowed(app_url):
    response = requests.patch(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


@pytest.mark.parametrize("user_id", [21])
def test_get_method_non_existed_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "kssdf"])
def test_get_method_unprocessable_entity(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_delete_method(app_url, user_id):
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NO_CONTENT
