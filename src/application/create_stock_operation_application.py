from src.application.base_application import BaseApplicatoin
from ..models.schema.stock import StockOperationReponse, stock_operation_response


class CreateStockOperation(BaseApplicatoin):

    async def execute(self, stock_symbol: str, amount: float) -> StockOperationReponse:
        try:
            return stock_operation_response(amount=amount, stock_symbol=stock_symbol)

        except Exception as e:
            raise e
