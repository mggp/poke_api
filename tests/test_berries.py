from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
@patch("app.routers.berries.BerryClient")
async def test_all_berry_stats_success(mock_berry_client):
    """Test that the /allBerryStats endpoint returns the correct statistics"""

    class MockBerry:
        def __init__(self, name, growth_time):
            self.name = name
            self.growth_time = growth_time

    berries = [MockBerry("cheri", 3), MockBerry("pecha", 4)]
    mock_berry_client.return_value.get_all_details = AsyncMock(return_value=berries)

    response = client.get("/allBerryStats")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data == {
        "berries_names": ["cheri", "pecha"],
        "min_growth_time": 3,
        "median_growth_time": 3.5,
        "max_growth_time": 4,
        "variance_growth_time": 0.25,
        "mean_growth_time": 3.5,
        "frequency_growth_time": {"3": 1, "4": 1},
    }


@pytest.mark.asyncio
@patch("app.routers.berries.BerryClient")
async def test_all_berry_stats_httpx_error(mock_berry_client):
    """Test that BerryClient raises an HTTPStatusError when there is
    an issue with the API request."""
    mock_berry_client.return_value.get_all_details = AsyncMock(
        side_effect=httpx.HTTPStatusError("error", request=None, response=None)
    )

    response = client.get("/allBerryStats")

    assert response.status_code >= 400


@pytest.mark.asyncio
@patch("app.routers.berries.BerryClient")
async def test_all_berry_stats_empty(mock_berry_client):
    """Test that the /allBerryStats endpoint returns empty statistics
    when no berries are found."""
    mock_berry_client.return_value.get_all_details = AsyncMock(return_value=[])
    response = client.get("/allBerryStats")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "berries_names": [],
        "min_growth_time": None,
        "median_growth_time": None,
        "max_growth_time": None,
        "variance_growth_time": None,
        "mean_growth_time": None,
        "frequency_growth_time": {},
    }
