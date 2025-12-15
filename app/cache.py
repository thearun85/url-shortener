from app.redis_client import get_redis
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_url_to_cache(short_code: str, detail: str, ttl: int=3600):
    redis_session = get_redis()
    logger.info(f"inside save_url_to_cache with ket {short_code}")
    redis_session.setex(f"url:{short_code}", ttl, json.dumps(detail))

def get_url_from_cache(short_code: str)->str | None:
    redis_session = get_redis()
    return redis_session.get(f"url:{short_code}")
