from fastapi.testclient import TestClient
from routes import router

client = TestClient(router)

def test_read_item():
    response = client.post(
        "/predict", 
        json={
            "Region": "northwest",
            "Gender": "female",
            "Smoker": "yes",
            "Children": 4,
            "Age": 20,
            "Bmi": 20
        }
    )
    assert response.status_code == 200
    assert response.json() != None