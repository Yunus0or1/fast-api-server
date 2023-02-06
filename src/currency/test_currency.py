
from fastapi.testclient import TestClient
from src.currency.models.currency_model import CurrencyRequest
from src.currency.service import get_app
from src.currency.util.log import log

app = get_app()
client = TestClient(app)
headers = {"x-token": "fake-super-secret-token"}


def test_default():
    response = client.get("/currency/", headers=headers)
    assert response.status_code == 200


def test_currency_converter_1():
    currency_request = CurrencyRequest(
        init_currency="GBP", target_currency="USD", amount=10)
    response = client.post("/currency/convert/",
                           headers=headers, json=currency_request.to_json())
    assert response.status_code == 200


def test_currency_converter_2():
    currency_request = CurrencyRequest(
        init_currency="GBPs", target_currency="USD", amount=10)
    response = client.post("/currency/convert/",
                           headers=headers, json=currency_request.to_json())
    assert response.status_code == 400

def test_currency_converter_3():
    currency_request = CurrencyRequest(
        init_currency="GBPs", target_currency="USD", amount=-1)
    response = client.post("/currency/convert/",
                           headers=headers, json=currency_request.to_json())
    result = response.json()
    assert result['message'] == 'The amount must be greater than 0.'
    assert response.status_code == 400


def test_currency_converter_4():
    currency_request = CurrencyRequest(
        init_currency="GBP", target_currency="USD", amount=10000000000000000000000)
    response = client.post("/currency/convert/",
                           headers=headers, json=currency_request.to_json())
    result = response.json()
    print(result)
    assert result['message'] == 'The amount is too big.'
    assert response.status_code == 400

