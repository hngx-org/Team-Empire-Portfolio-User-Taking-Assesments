from .main import app
import requests
from fastapi.testclient import TestClient


def login():
    response = requests.post(
        "https://staging.zuri.team/api/auth/api/auth/login",
        data={
          "email":"abdulrasheedabdulsalam706@gmail.com",
          "password": "@Testing123"
        }
    )
    return response.json().get("data").get("token")

client = TestClient(app, headers={"token": f"{login()}"})

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_user_assessment():
    response = client.get("/api/assessments")
    assert response.status_code == 200
    assert len(response.json()) > 0
    # Still wprking on it
