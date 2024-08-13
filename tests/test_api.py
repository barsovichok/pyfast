import json
from http import HTTPStatus
from logging import log

import pytest
from app.models.User import User
import requests

payload = {
    "email": "3242@gmail.com",
    "first_name": "FirstName",
    "last_name": "LastName",
    "avatar": "https://reqres.in/png/faces/1383-image.jpg"
}


@pytest.fixture(scope="module")
def json_payloads(app_url):
    with open("users.json") as f:
        test_data_payloads = json.load(f)
        return test_data_payloads


@pytest.fixture(scope="module")
def fill_test_data(app_url):
    with open("users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        response = requests.delete(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NO_CONTENT


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


def test_post_method(app_url, json_payloads):
    for json_payload in (json_payloads[0], json_payloads[-1]):
        response = requests.post(f"{app_url}/api/users/", json=json_payload)
        assert response.status_code == HTTPStatus.CREATED
        User.model_validate(response.json())


# def test_patch_method(app_url, fill_test_data):
#     for user_id in (fill_test_data[0], fill_test_data[-1]):
#         response = requests.patch(f"{app_url}/api/users/{user_id}", data=json.dumps(payload))
#         assert response.status_code == HTTPStatus.OK
#         User.model_validate(response.json())


def test_get_method(app_url, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        User.model_validate(response.json())


def test_get_method_not_allowed(app_url):
    response = requests.patch(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_get_method_non_existed_values(app_url, json_payloads):
    create_response = requests.post(f"{app_url}/api/users/", json=json_payloads[0]).json()
    user_id = create_response["id"]
    requests.delete(f"{app_url}/api/users/{user_id}")
    response = requests.get(f"{app_url}/api/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "kssdf"])
def test_get_method_unprocessable_entity(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_delete_method(app_url, json_payloads):
    for json_payload in (json_payloads[0], json_payloads[-1]):
        create_response = requests.post(f"{app_url}/api/users/", json=json_payload).json()
        user_id = create_response["id"]
        response = requests.delete(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NO_CONTENT
