from src.application.base_application import BaseApplicatoin

from ..infra.connectors.polygon import PolygonConnect
from ..models.schema.stock import StockResponse, stock_adapter


class StockApplication(BaseApplicatoin):
    async def execute(self, stock_symbol: str) -> StockResponse:

        test_date = "2023-08-08"
        try:
            polygon_resp = await PolygonConnect().get_open_close(
                stock=stock_symbol, date=test_date
            )
            print(polygon_resp)
            return stock_adapter(polygon_resp)

        except Exception as e:
            raise e
