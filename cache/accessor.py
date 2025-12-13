import os

import redis
from settings import Settings




def get_redis_connection() -> redis.Redis:
    setings = Settings()
    return redis.Redis(
        host=setings.CACHE_HOST,
        port=setings.CACHE_PORT,
        db= setings.CACHE_DB)


def set_pomodoro_counts():
    redis = get_redis_connection()
    redis.set('pomodoro_counts', 1)