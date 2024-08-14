from http import HTTPStatus

import requests

from app.models.User import UserCreate, User


def test_post_method(app_url, json_payloads):
    for json_payload in (json_payloads[0], json_payloads[-1]):
        UserCreate.model_validate(json_payload)
        response = requests.post(f"{app_url}/api/users/", json=json_payload)
        assert response.status_code == HTTPStatus.CREATED
        User.model_validate(response.json())


def test_get_created_item(app_url, json_payloads):
    for json_payload in (json_payloads[0], json_payloads[-1]):
        UserCreate.model_validate(json_payload)
        response = requests.post(f"{app_url}/api/users/", json=json_payload)
        assert response.status_code == HTTPStatus.CREATED
        User.model_validate(response.json())
        user_id = response.json()["id"]
        get_response = requests.get(f"{app_url}/api/users/{user_id}")
        assert get_response.status_code == HTTPStatus.OK
        assert get_response.json()["id"] == user_id
        assert get_response.json()["email"] == json_payload["email"]
        assert get_response.json()["first_name"] == json_payload["first_name"]
        assert get_response.json()["last_name"] == json_payload["last_name"]
        assert get_response.json()["avatar"] == json_payload["avatar"]


def test_validate_email(app_url, json_payloads):
    for json_payload in (json_payloads[0], json_payloads[-1]):
        json_payload["email"] = "invalid_email"
        response = requests.post(f"{app_url}/api/users/", json=json_payload)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_validate_avatar(app_url, json_payloads):
    for json_payload in (json_payloads[0], json_payloads[-1]):
        json_payload["avatar"] = "invalid_url"
        response = requests.post(f"{app_url}/api/users/", json=json_payload)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_first_name_missed(app_url, json_payloads):
    for json_payload in (json_payloads[0], json_payloads[-1]):
        del json_payload["first_name"]
        response = requests.post(f"{app_url}/api/users/", json=json_payload)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_last_name_missed(app_url, json_payloads):
    for json_payload in (json_payloads[0], json_payloads[-1]):
        del json_payload["last_name"]
        response = requests.post(f"{app_url}/api/users/", json=json_payload)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_empty_payload(app_url):
    response = requests.post(f"{app_url}/api/users/", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_method_not_allowed(app_url):
    response = requests.put(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
