import logging
import time
import os
from app.db import init_db, get_session
from app.redis_client import init_redis
from app.models import Click
from app.queue import get_pending_clicks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BATCH_SIZE = 100
POLL_INTERVAL = 1

def processClicks()->int:
    clicks = get_pending_clicks(BATCH_SIZE)
    if not clicks:
        return 0
        
    session = get_session()
    try:
        for click_data in clicks:
            click = Click(
                url_id = click_data["url_id"],
                clicked_at = click_data["clicked_at"]
            )
            session.add(click)
        session.commit()
        logger.info(f"Inserted {len(clicks)} clicks")
        return len(clicks)
    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting clicks: {e}")
        return 0
    finally:
        session.close()

def main():
    logger.info("Starting Async Worker process")
    
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        init_db(database_url)
        
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        init_redis(redis_url)
        
    while True:
        processed = processClicks()
        if processed == 0:
            time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    main()
