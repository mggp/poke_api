import pickle

import pytest

import app.utils.cache as cache_module
from app.config import redis_settings


@pytest.fixture
def mock_redis_client(mocker):
    mock_client = mocker.Mock()
    mocker.patch.object(cache_module, "REDIS_CLIENT", mock_client)
    return mock_client


@pytest.fixture
def mock_redis_settings(mocker):
    settings = mocker.Mock()
    settings.enabled = True
    settings.host = "localhost"
    settings.port = 6379
    settings.db = 0
    settings.password = None
    settings.default_expiration = 123
    mocker.patch.object(cache_module, "redis_settings", settings)
    return settings


@pytest.fixture
def cache_prefix(mocker):
    mocker.patch.object(cache_module, "CACHE_PREFIX", "testprefix:")


@pytest.mark.asyncio
async def test_cache_hit_returns_cached_value(mock_redis_client, cache_prefix):
    value = {"foo": "bar"}
    mock_redis_client.get.return_value = pickle.dumps(value)

    @cache_module.cache("mykey")
    async def func():
        return {"should_not": "be called"}

    result = await func()

    assert result == value
    mock_redis_client.get.assert_called_once_with("testprefix:mykey")
    mock_redis_client.set.assert_not_called()


@pytest.mark.asyncio
async def test_cache_miss_calls_function_and_sets_cache(
    mock_redis_client, cache_prefix
):
    value = [1, 2, 3]
    mock_redis_client.get.return_value = None
    called = {"called": False}

    @cache_module.cache("otherkey", expire_seconds=10)
    async def func():
        called["called"] = True
        return value

    result = await func()

    assert result == value
    mock_redis_client.get.assert_called_once_with("testprefix:otherkey")
    mock_redis_client.set.assert_called_once()
    args, kwargs = mock_redis_client.set.call_args
    assert args[0] == "testprefix:otherkey"
    assert pickle.loads(args[1]) == value
    assert kwargs["nx"] is True
    assert kwargs["ex"] == 10
    assert called["called"] is True


@pytest.mark.asyncio
async def test_cache_returns_func_result_when_redis_disabled(mocker, cache_prefix):
    mocker.patch.object(redis_settings, "enabled", False)
    called = {"called": False}

    @cache_module.cache("nokey")
    async def func():
        called["called"] = True
        return "abc"

    result = await func()
    assert result == "abc"
    assert called["called"] is True
