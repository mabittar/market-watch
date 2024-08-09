import json

from pytest import mark


@mark.anyio
async def test_get_stock(async_client):
    symbol = "AAPL"
    expected_response = {"stockSymbol": symbol}
    expected_status_code = 200
    response = await async_client.get(f"/stock/{symbol}")
    assert response.status_code == expected_status_code
    parsedResponse = json.loads(response.content)
    assert parsedResponse["companyCode"] == symbol
