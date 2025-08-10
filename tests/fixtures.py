import pytest


@pytest.fixture
def base_settings(monkeypatch):
    """Fixture to mock settings for testing."""

    monkeypatch.setattr("app.config.settings.poke_api_path", "http://fakeapi.co/api")
    monkeypatch.setattr("app.config.settings.float_decimal_places", 2)


class MockBerry:
    def __init__(self, name, growth_time):
        self.name = name
        self.growth_time = growth_time


@pytest.fixture
def get_all_berries_mock(mocker):
    """Fixture to mock BerryClient for testing."""
    all_berries_data = [MockBerry("cheri", 3), MockBerry("pecha", 4)]

    mock_berry_client = mocker.AsyncMock()
    mock_berry_client.get_all_details.side_effect = [all_berries_data]

    mocker.patch("app.routers.berries.BerryClient", return_value=mock_berry_client)
