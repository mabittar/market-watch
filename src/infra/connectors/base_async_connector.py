from typing import Any

import httpx

from ...exceptions import ConnectorError


class BaseAsyncConnector:
    def httpx_url_converter(self, url: str) -> httpx.URL:
        return httpx.URL(url)

    async def request_async(  # noqa
        self, url=httpx.URL(), method=None, headers=None, timeout=None, **kwargs
    ) -> Any:  # noqa
        async with httpx.AsyncClient() as client:
            if method == "GET":
                resp = await client.get(
                    url,
                    headers=headers,
                    timeout=timeout,
                )

                if resp.status_code != 200:  # noqa
                    raise ConnectorError(
                        error_msg=resp.text, status_code=resp.status_code
                    )
            else:
                raise Exception("Undefined request method")
        return resp.json()
