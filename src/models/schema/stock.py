from pydantic import BaseModel

from .base import BaseSchemaModel


class StockOperation(BaseModel):
    amount: float


class StockOperationReponse(BaseSchemaModel):
    message: str


def stock_operation_response(amount: float, stock_symbol: str) -> StockOperationReponse:
    return StockOperationReponse(
        message=f"{amount} units of stock {stock_symbol} were added to your stock record"
    )


class StockValues(BaseSchemaModel):
    open: float
    high: float
    low: float
    close: float


class StockResponse(BaseSchemaModel):
    status: str
    company_code: str
    request_data: str
    stock_values: StockValues


def stock_adapter(polygon_resp: dict) -> StockResponse:
    stock_values = StockValues(
        open=float(polygon_resp.get("open", 0)),
        high=float(polygon_resp.get("high", 0)),
        low=float(polygon_resp.get("low", 0)),
        close=float(polygon_resp.get("close", 0)),
    )
    return StockResponse(
        status=polygon_resp.get("status", "Error"),
        company_code=polygon_resp.get("symbol", "X"),
        request_data=polygon_resp.get("from", ""),
        stock_values=stock_values,
    )
