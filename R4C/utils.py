from django.conf import settings
import redis


def connect_redis():
    r = redis.StrictRedis(host=settings.REDIS_HOST,
                          port=settings.REDIS_PORT,
                          decode_responses=True)
    return r
