import json
import time

import requests
from jsonschema import validate
from schemas import default_user

url = "http://127.0.0.1:8000/api"

payload = {
    "email": "test@test.test",
    "first_name": "FirstName",
    "last_name": "LastName",
    "avatar": "4"
}


def test_post_method():
    response = requests.post(url + "/users/", data=json.dumps(payload))
    body = response.json()
    assert response.status_code == 201
    validate(body, schema=default_user)


def test_put_method():
    response = requests.put(url + "/users/" + str(int(time.time())), data=json.dumps(payload))
    assert response.status_code == 200


def test_get_method():
    random_id = str(int(time.time()))
    response = requests.get(url + "/users/" + random_id)
    assert response.status_code == 200
    validate(response.json(), schema=default_user)


def test_get_method_not_allowed():
    response = requests.get(url + "/users/")
    assert response.status_code == 405


def test_get_method_not_found():
    response = requests.get(url)
    assert response.status_code == 404


def test_get_method_unprocessable_entity():
    response = requests.get(url + "/users/" + "j")
    assert response.status_code == 422


def test_delete_method():
    random_id = str(int(time.time()))
    response = requests.delete(url + "/users/" + random_id)
    assert response.status_code == 204
