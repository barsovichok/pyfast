import json
import time

import requests
from jsonschema import validate

from schemas import default_user

url = "http://127.0.0.1:8000/api/users/"

payload = {
    "email": "test@test.test",
    "first_name": "FirstName",
    "last_name": "LastName",
    "avatar": "4"
}


def test_post_method():
    response = requests.post(url, data=json.dumps(payload))
    body = response.json()
    assert response.status_code == 200
    validate(body, schema=default_user)


def test_put_method():
    response = requests.put(url + str(int(time.time())), data=json.dumps(payload))
    assert response.status_code == 200


def test_get_method():
    random_id = str(int(time.time()))
    response = requests.get(url + random_id)
    assert response.status_code == 200
    validate(response.json(), schema=default_user)