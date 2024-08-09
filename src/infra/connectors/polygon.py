from fastapi import HTTPException
from httpx import Response

from ...exceptions import ConnectorError
from ...settings import settings
from .base_async_connector import BaseAsyncConnector


class PolygonConnect(BaseAsyncConnector):
    api_key = settings.POLYGON_API_KEY

    async def get_open_close(self, stock: str, date: str | None) -> dict:
        try:
            headers = {
                "content-type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
            url = f"https://api.polygon.io/v1/open-close/{stock}/{date}"
            httpx_url = self.httpx_url_converter(url)
            resp: Response = await self.request_async(
                method="GET",
                url=httpx_url,
                headers=headers,
                timeout=settings.POLYGON_API_TIMEOUT,
            )

            if resp.status_code != 200:  # noqa
                raise ConnectorError(error_msg=resp.text, status_code=resp.status_code)

            return resp.json()

        except HTTPException as e:
            raise e
