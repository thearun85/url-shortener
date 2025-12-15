from app.redis_client import get_redis
import json
from datetime import datetime, timezone

CLICKS_QUEUE = "clicks_queue"

def add_to_queue(url_id: int):
    redis_session = get_redis()
    clicked_at = datetime.now(timezone.utc).isoformat()
    data = json.dumps({"url_id": url_id, "clicked_at": clicked_at,})
    redis_session.rpush(CLICKS_QUEUE, data)

def get_pending_clicks(batch_size: int)->[]:
    clicks = []
    redis_session = get_redis()
    for _ in range(batch_size):
        data = redis_session.lpop(CLICKS_QUEUE)
        if not data:
            break
        clicks.append(json.loads(data))
    return clicks
