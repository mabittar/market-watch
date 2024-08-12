from fastapi import HTTPException, status

from ..application.base_application import BaseApplicatoin
from ..infra.data.repositories.stock_repository import StockRepository
from ..infra.db.session import DBSessionDep
from ..models.schema.stock import StockResponse, make_operation_response


class GetStockOperationApplication(BaseApplicatoin):

    async def execute(
        self,
        stock_symbol: str,
        date: str,
        db_session: DBSessionDep,
    ) -> StockResponse:
        stock_repo = StockRepository(db_session)
        try:
            stock = await stock_repo.get_stock_by_company_code(stock_symbol)
            if stock is None or stock.id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"can not find {stock_symbol}, create an operation first",
                )
            operation = await stock_repo.get_stock_operation_by_date(
                str(stock.id), date
            )
            if operation is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"can not find operation for date: {date}, create an operation first",
                )
            stock_ts = await stock_repo.get_stock_timeseries(str(stock.id))
            stock_market_cap = await stock_repo.get_market_cap(str(stock.id))
            stock_performace = await stock_repo.get_stock_performance(str(stock.id), date)
            stock_competitors = await stock_repo.get_competitors(str(stock.id))

            return make_operation_response(
                stock,
                stock_ts,
                stock_market_cap,
                stock_performace,
                stock_competitors,
                operation,
            )

        except Exception as e:
            raise e
