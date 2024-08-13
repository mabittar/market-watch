
from pydantic import BaseModel, Field

from src.infra.data.entities.stock import (
    Stock,
    StockOperation,
)

from ...utils.market_cap_value_parser import CurrencyValueAdapter
from .base import BaseSchemaModel


class StockOperationRequest(BaseModel):
    amount: float
    date: str | None = Field(
        default=None, description="operation date, must be YYYY-MM-DD"
    )


class StockOperationReponse(BaseSchemaModel):
    message: str


def stock_operation_response(
    amount: float, stock_symbol: str, **kwargs
) -> StockOperationReponse:
    return StockOperationReponse(
        message=f"{amount} units of stock {stock_symbol} were added to your stock record"
    )


class StockValuesSchema(BaseModel):
    open: float
    high: float
    low: float
    close: float
    date: str


class StockPerformanceSchema(BaseModel):
    five_days: float
    one_month: float
    three_months: float
    year_to_date: float
    one_year: float


class CompetitorSchema(BaseModel):
    name: str


class StockMarketCapSchema(BaseModel):
    currency: str
    value: float


class StockResponse(BaseSchemaModel):
    status: str
    company_code: str
    company_name: str
    request_data: str
    purchased_amount: float
    purchased_status: str
    stock_values: list[StockValuesSchema]
    performance_data: StockPerformanceSchema
    market_cap: StockMarketCapSchema
    competitors: list[CompetitorSchema]


def parse_market_cap(marketcap: str) -> StockMarketCapSchema:
    parsed = CurrencyValueAdapter.convert(marketcap)
    return StockMarketCapSchema(**parsed)


def _parse_percentage(value: str) -> float:
    # Remove o símbolo de porcentagem e converte para float
    return float(value.strip("%")) if value else 0.0


def build(
    polygon_resp: dict, market_watch_resp: dict, amount: float, date_str: str
) -> StockResponse:
    performance = StockPerformanceSchema(
        five_days=_parse_percentage(market_watch_resp["performance"].get("5 Day", 0)),
        one_month=_parse_percentage(market_watch_resp["performance"].get("1 Month", 0)),
        three_months=_parse_percentage(
            market_watch_resp["performance"].get("3 Month", 0)
        ),
        year_to_date=_parse_percentage(market_watch_resp["performance"].get("YTD", 0)),
        one_year=_parse_percentage(market_watch_resp["performance"].get("1 Year", 0)),
    )

    market_cap = parse_market_cap(market_watch_resp["market_cap"])
    competitors: list[CompetitorSchema] = [
        CompetitorSchema(name=competitor)
        for competitor in market_watch_resp["competitors"]
    ]
    stock_values = StockValuesSchema(
        open=float(polygon_resp.get("open", 0)),
        high=float(polygon_resp.get("high", 0)),
        low=float(polygon_resp.get("low", 0)),
        close=float(polygon_resp.get("close", 0)),
        date=date_str,
    )
    return StockResponse(
        status=polygon_resp.get("status", "Error"),
        company_code=polygon_resp.get("symbol", "X"),
        request_data=polygon_resp.get("from", ""),
        stock_values=[stock_values],
        performance_data=performance,
        market_cap=market_cap,
        competitors=competitors,
        purchased_amount=amount,
        purchased_status="Done",
        company_name=market_watch_resp["company_name"],
    )


def make_operation_response(
    stock: Stock,
    stock_ts: list[StockValuesSchema],
    stock_market_cap: StockMarketCapSchema,
    stock_performace: StockPerformanceSchema,
    stock_competitors: list[CompetitorSchema],
    operation: StockOperation,
) -> StockResponse:
    return StockResponse(
        competitors=stock_competitors,
        market_cap=stock_market_cap,
        performance_data=stock_performace,
        stock_values=stock_ts,
        company_code=str(stock.company_code),
        company_name=str(stock.company_name),
        purchased_amount=float(operation.purchased_amount),  # type: ignore
        purchased_status=str(operation.purchased_status),
        request_data=str(operation.operation_date),
        status=str(operation.purchased_status),
    )
