
from fastapi.testclient import TestClient
from src.currency.service import get_app

app = get_app()
client = TestClient(app)
headers = {"x-token": "fake-super-secret-token"}

def test_default():
    response = client.get("/currency/", headers=headers)
    print(response)
    assert response.status_code == 200
