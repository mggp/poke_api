import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, AsyncMock
import httpx

client = TestClient(app)

@pytest.mark.asyncio
@patch("app.routers.berries.BerryClient")
async def test_all_berry_stats_success(mock_berry_client):
    class MockBerry:
        def __init__(self, name, growth_time):
            self.name = name
            self.growth_time = growth_time
    berries = [MockBerry("cheri", 3), MockBerry("pecha", 4)]
    mock_berry_client.return_value.get_all_details = AsyncMock(return_value=berries)

    response = client.get("/allBerryStats")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["berries_names"] == ["cheri", "pecha"]
    assert data["min_growth_time"] == 3
    assert data["max_growth_time"] == 4
    assert data["mean_growth_time"] == 3.5
    assert data["median_growth_time"] == 3.5
    assert data["variance_growth_time"] == 0.25
    assert data["frequency_growth_time"] == {"3": 1, "4": 1}

@pytest.mark.asyncio
@patch("app.routers.berries.BerryClient")
async def test_all_berry_stats_httpx_error(mock_berry_client):
    mock_berry_client.return_value.get_all_details = AsyncMock(side_effect=httpx.HTTPStatusError("error", request=None, response=None))
    response = client.get("/allBerryStats")
    assert response.status_code >= 400

@pytest.mark.asyncio
@patch("app.routers.berries.BerryClient")
async def test_all_berry_stats_empty(mock_berry_client):
    mock_berry_client.return_value.get_all_details = AsyncMock(return_value=[])
    response = client.get("/allBerryStats")
    assert response.status_code == 200
    data = response.json()
    assert data == {}
