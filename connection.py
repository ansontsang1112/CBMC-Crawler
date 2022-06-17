import redis
import main as m


def redis_init():
    try:
        conn = redis.Redis(host=m.REDIS_URL, port=m.REDIS_PORT, db=m.REDIS_DATABASE)
    except ConnectionError:
        conn = None

    return conn
