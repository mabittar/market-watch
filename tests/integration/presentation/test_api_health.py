import json

from pytest import mark


@mark.anyio
async def test_api_health_check_healthy(async_client):
    expected_response = {"status": "💚"}
    expected_status_code = 200
    response = await async_client.get("/health")
    assert response.status_code == expected_status_code
    assert json.loads(response.content) == expected_response
