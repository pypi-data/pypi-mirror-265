import redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry


def get_redis_client(redis_config: dict, cap=0.512, base=0.008, retries=60):
    if redis_config is None:
        raise ValueError(f"redis config is None")
    retry = Retry(ExponentialBackoff(cap=cap, base=base), retries=retries)
    redis_param = dict(
        charset="UTF-8",
        encoding="UTF-8",
        decode_responses=True,
        health_check_interval=60,
        retry=retry,
        retry_on_error=[redis.BusyLoadingError, redis.ConnectionError, redis.TimeoutError],
    )
    redis_param.update(redis_config)
    rdc = redis.Redis(**redis_param)
    return rdc
