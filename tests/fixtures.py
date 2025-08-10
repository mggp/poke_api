import pytest


@pytest.fixture
def base_settings(monkeypatch):
    """Fixture to mock settings for testing."""

    monkeypatch.setattr("app.config.settings.poke_api_path", "http://fakeapi.co/api")
    monkeypatch.setattr("app.config.settings.float_decimal_places", 2)
