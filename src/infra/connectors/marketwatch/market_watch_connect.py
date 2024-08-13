from fastapi import HTTPException

from src.infra.connectors.marketwatch.market_watch_client import MarketWatchClient


class MarketWatchConnect:
    async def get_market_data(self, stock: str) -> dict:
        try:
            market_client = MarketWatchClient()
            return market_client.get_maktet_data(stock)

        except HTTPException as e:
            raise e
