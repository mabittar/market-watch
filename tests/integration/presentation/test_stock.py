import json

from pytest import mark


@mark.anyio
async def test_get_stock(async_client):
    symbol = "AAPL"
    expected_status_code = 200
    response = await async_client.get(f"/stock/{symbol}")
    assert response.status_code == expected_status_code
    parsedResponse = json.loads(response.content)
    assert parsedResponse["companyCode"] == symbol


@mark.anyio
async def test_get_stock_symbol_too_short(async_client):
    symbol = "A"
    expected_status_code = 400
    response = await async_client.get(f"/stock/{symbol}")
    assert response.status_code == expected_status_code
    parsed_response = json.loads(response.content)
    assert parsed_response["detail"] == "stock_symbol must be greater than 2 letters"


@mark.anyio
async def test_create_stock_operation_symbol_too_short(async_client):
    symbol = "A"
    payload = {"amount": 100}
    expected_status_code = 400
    response = await async_client.post(f"/stock/{symbol}", json=payload)
    assert response.status_code == expected_status_code
    parsed_response = json.loads(response.content)
    assert parsed_response["detail"] == "stock_symbol must be greater than 2 letters"
