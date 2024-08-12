import requests


def test_status(app_url):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == 200
    data = response.json()
    assert data["users"] is True
