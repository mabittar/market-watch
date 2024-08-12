from datetime import datetime, timedelta

from ..infra.connectors import MarketWatchConnect, PolygonConnect
from ..infra.data.repositories.stock_repository import StockRepository
from ..infra.db.session import DBSessionDep
from ..models.schema.stock import (
    StockOperationReponse,
    StockOperationRequest,
    build,
    stock_operation_response,
)
from .base_application import BaseApplicatoin


class CreateStockOperation(BaseApplicatoin):

    def get_last_b_day(self) -> str:
        sunday = 0
        saturday = 6
        actual_date = datetime.now()
        diff = 1
        if actual_date.weekday() == sunday:
            diff = 3
        elif actual_date.weekday() == saturday:
            diff = 2
        else:
            diff = 1
        operation_date = datetime.now() - timedelta(diff)
        return datetime.strftime(operation_date, "%Y-%m-%d")

    async def execute(
        self,
        operation: StockOperationRequest,
        stock_symbol: str,
        db_session: DBSessionDep,
    ) -> StockOperationReponse:
        if operation.date is not None:
            date_str = operation.date
        else:
            date_str = self.get_last_b_day()
        amount = operation.amount
        stock_repo = StockRepository(db_session)
        try:
            polygon_resp = await PolygonConnect().get_open_close(
                stock=stock_symbol, date=date_str
            )
            market_watch_resp = await MarketWatchConnect().get_market_data(stock_symbol)
            stock = build(polygon_resp, market_watch_resp, amount, date_str)
            print(stock)
            stock_dump = stock.model_dump()
            db_stock = await stock_repo.add_stock(**stock_dump)
            stock_id = str(db_stock.id)
            await stock_repo.add_stock_timeseries(
                **stock_dump["stock_values"][0], stock_id=stock_id, date_str=date_str
            )
            await stock_repo.add_market_cap(
                **stock_dump["market_cap"], stock_id=stock_id, date_str=date_str
            )
            await stock_repo.add_stock_performance(
                **stock_dump["performance_data"], stock_id=stock_id, date_str=date_str
            )
            await stock_repo.add_stock_operation(**stock_dump, stock_id=stock_id)
            for competitor in stock.competitors:
                await stock_repo.add_competitor(stock_id=stock_id, name=competitor.name)
            return stock_operation_response(stock_symbol=stock_symbol, amount=amount)

        except Exception as e:
            raise e
