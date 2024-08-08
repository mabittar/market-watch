import json

from pytest import mark


@mark.anyio
async def test_api_health_check_healthy(async_client):
    expected_response = {"status": "💚"}
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert json.loads(response.content) == expected_response
