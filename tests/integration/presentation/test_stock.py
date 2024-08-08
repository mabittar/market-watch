import json

from pytest import mark


@mark.anyio
async def test_get_stock(async_client):
    symbol = "AAPL"
    expected_response = {"stock_symbol": symbol}
    response = await async_client.get(f"/stock/{symbol}")
    assert response.status_code == 200
    assert json.loads(response.content) == expected_response
