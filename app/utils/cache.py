import logging
import pickle
from functools import wraps

from redis import Redis

from app.config import redis_settings
from app.constants import CACHE_PREFIX

logger = logging.getLogger(__name__)

if redis_settings.enabled:
    REDIS_CLIENT = Redis(
        host=redis_settings.host,
        port=redis_settings.port,
        db=redis_settings.db,
        password=redis_settings.password,
        ssl=redis_settings.use_ssl,
    )
else:
    REDIS_CLIENT = None


def cache(key, expire_seconds: int = None):
    """Decorator to cache the result of a function in Redis."""
    if expire_seconds is None:
        expire_seconds = redis_settings.default_expiration

    cache_key = f"{CACHE_PREFIX}{key}"

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if REDIS_CLIENT is None:
                return await func(*args, **kwargs)

            cached_data = REDIS_CLIENT.get(cache_key)

            if cached_data:
                logger.debug(
                    "Cache hit for function %s with key %s", func.__name__, key
                )
                return pickle.loads(cached_data)

            result = await func(*args, **kwargs)
            REDIS_CLIENT.set(
                cache_key, pickle.dumps(result), nx=True, ex=expire_seconds
            )

            return result

        return wrapper

    return decorator
