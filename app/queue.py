from app.redis_client import get_redis
import json

CLICKS_QUEUE = "clicks_queue"

def add_to_queue(url_id: int):
    redis_session = get_redis()
    data = json.dumps({"url_id": url_id,})
    redis_session.rpush(CLICKS_QUEUE, data)
