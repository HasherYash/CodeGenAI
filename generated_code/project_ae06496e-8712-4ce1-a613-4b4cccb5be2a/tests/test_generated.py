Here are the pytest unit tests for the provided FastAPI app code:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_login(client):
    response = client.post("/login", json={"email": "test@example.com", "password": "test_password"})
    assert response.status_code == 200
    assert response.json() == {"token": "jwt-token-here", "user": {"id": 1, "role": "manager"}}

def test_get_current_user(client):
    response = client.get("/user", headers={"Authorization": "Bearer jwt-token-here"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "role": "manager"}

def test_get_dashboard_tiles(client):
    response = client.get("/tiles", headers={"Authorization": "Bearer jwt-token-here"})
    assert response.status_code == 200
    assert response.json() == []

def test_apply_for_leave(client):
    response = client.post("/leaves/apply", json={"start_date": "2022-01-01", "end_date": "2022-01-31", "reason": "Test leave"})
    assert response.status_code == 200
    assert response.json() == {"message": "Leave request submitted successfully", "status": "pending"}

def test_approve_leave(client):
    response = client.patch("/leaves/1/approve", json={"status": "approved"})
    assert response.status_code == 200
    assert response.json() == {"message": "Leave request approved", "status": "approved"}

def test_get_pod_details(client):
    response = client.get("/pods/1/details", headers={"Authorization": "Bearer jwt-token-here"})
    assert response.status_code == 200
    assert response.json() == {"pod_id": "56789", "pod_name": "Innovation Team", "members": [1, 2, 3]}

def test_recommend_employee(client):
    response = client.post("/pods/1/recommend", json={"recommended_user_id": 2})
    assert response.status_code == 200
    assert response.json() == {"message": "Recommendation sent successfully"}
```

Note that you will need to implement the logic for each endpoint and add error handling and validation as needed.