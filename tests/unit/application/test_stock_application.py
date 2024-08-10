# tests/test_stock_application.py
import pytest

from src.application.stock_application import StockApplication
from src.infra.connectors.base_async_connector import BaseAsyncConnector


@pytest.mark.anyio
async def test_stock_application_execute(mocker):
    expected_polygon_response = {
        "status": "OK",
        "from": "2023-08-08",
        "symbol": "AAPL",
        "open": 179.69,
        "high": 180.27,
        "low": 177.58,
        "close": 179.8,
        "volume": 67769003.0,
        "afterHours": 179.79,
        "preMarket": 178.78,
    }

    mocker.patch.object(
        BaseAsyncConnector, "request_async", return_value=expected_polygon_response
    )

    stock_application = StockApplication()
    result = await stock_application.execute("AAPL")

    assert result.company_code == "AAPL"
    assert result.stock_values.open == expected_polygon_response["open"]
    assert result.stock_values.close == expected_polygon_response["close"]
