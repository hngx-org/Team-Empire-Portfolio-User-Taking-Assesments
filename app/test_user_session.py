from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.services.user_session import AssessmentSessionData, SessionData, save_session, get_all_session, get_session_detail  # replace 'your_module_name' with the actual name of your module

test_app = FastAPI()

@test_app.post("/save_session/", status_code=201)
def save_endpoint(data: SessionData, user_id: int):
    return save_session(data, user_id)

@test_app.get("/get_all_session/{user_id}")
def get_all_endpoint(user_id: int):
    return get_all_session(user_id)

@test_app.get("/get_session_detail/{user_id}/{assessment_id}", response_model=AssessmentSessionData)
def get_detail_endpoint(user_id: int, assessment_id: int):
    return get_session_detail(user_id, assessment_id)

client = TestClient(test_app)

def test_save_session():
    response = client.post("/save_session/", json={
        "assessment_id": 1,
        "time_remaining": 20,
        "responses": [{
            "question_id": 1,
            "answer_id": 1
        }]
    }, params={"user_id": 1})

    assert response.status_code == 201
    assert response.json() == {"status_code": 201}

def test_get_all_session():
    response = client.get("/get_all_session/1")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["user_id"] == 1
    assert response.json()[0]["assessment_id"] == 1

def test_get_session_detail():
    response = client.get("/get_session_detail/1/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["questions"][0]["id"] == 1
    assert response.json()["questions"][0]["answer_id"] == 1

def test_get_session_detail_not_found():
    response = client.get("/get_session_detail/2/1")
    assert response.status_code == 404
