from http import HTTPStatus

import requests
import pytest
from test_api_routes import users
from models.User import User


def test_pagination_existed(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.json().get("items")
    assert response.json().get("page")
    assert response.json().get("total")
    assert response.json().get("size")
    assert response.json().get("pages")


def test_pagination_validate_items(app_url, users):
    response = requests.get(f"{app_url}/api/users")
    users = response.json().get("items")
    for user in users:
        User.model_validate(user)


def test_pagination_validate_default_values(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.json().get("items")
    assert response.json().get("page") == 1
    assert response.json().get("total") == len(response.json().get("items"))
    assert response.json().get("size") == 50
    assert response.json().get("pages") == 1


@pytest.mark.parametrize("page, size", [(2, 3), (3, 2), (4, 1)])
def test_pagination_validate_values(app_url, page, size, total, pagination, users):
    payload = {"page": page, "size": size}
    response = requests.get(f"{app_url}/api/users", params=payload)
    assert response.json().get("page") == page
    assert response.json().get("total") == total
    assert response.json().get("size") == size
    assert response.json().get("pages") == pagination


@pytest.mark.parametrize("page, size", [("sw", 20), (20, -1), (5, 0), (30, "$%%%$")])
def test_pagination_invalidate_values(app_url, page, size):
    payload = {"page": page, "size": size}
    response = requests.get(f"{app_url}/api/users", params=payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("page, size", [(4, 8), (9, 19), (10, 10)])
def test_pagination_no_values(app_url, users, page, size, total, pagination):
    payload = {"page": page, "size": size}
    response = requests.get(f"{app_url}/api/users", params=payload)
    assert response.json().get("items") == []
    assert response.json().get("page") == page
    assert response.json().get("total") == total
    assert response.json().get("size") == size
    assert response.json().get("pages") == pagination


@pytest.mark.parametrize("page, size", [(1, 10), (3, 4), (10, 2)])
def test_pagination_different_values(app_url, users, page, size):
    payload = {"page": page, "size": size}
    response = requests.get(f"{app_url}/api/users", params=payload)
    users = response.json().get("items")
    assert users[0]["id"] != users[-1]["id"]
