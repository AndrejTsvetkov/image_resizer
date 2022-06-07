from __future__ import annotations

from redis import Redis, from_url  # pylint: disable=unused-import
from redis.exceptions import ConnectionError as RedisConnectionError
from rq import Queue

from app.config import get_settings
from app.exceptions import ServiceUnavailable


def get_redis() -> 'Redis[bytes]':  # pragma: no cover, in tests we are using FakeRedis
    try:
        redis = from_url(get_settings().REDIS_URL)
        redis.ping()
        return redis
    except RedisConnectionError as err:
        raise ServiceUnavailable from err


def get_queue() -> Queue:
    return Queue(name='image_resizer', connection=get_redis())
