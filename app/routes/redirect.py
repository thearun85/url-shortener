from flask import Blueprint, jsonify, redirect
from app.db import get_session
from app.models import URL
from app.utils import validate_shortcode, url_redirects_total, cache_hits_total, cache_misses_total
from app.queue import add_to_queue
from app.cache import get_url_from_cache, save_url_to_cache
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redirect_bp = Blueprint("redirect", __name__)

@redirect_bp.route("/<short_code>", methods=["GET"])
def redirect_to_url(short_code):

    is_valid, error = validate_shortcode(short_code)
    if not is_valid:
        return jsonify({
            "error": error
        }), 400
    session = get_session()

    try:
        url_id = 0
        orig_url = None
        
        cache = get_url_from_cache(short_code)
        if not cache:
            logger.info(f"cache miss key is {short_code}")
            url = session.query(URL).filter_by(short_code=short_code).first()
            if not url:
                return jsonify({
                    "erorr": "URL not found"
                }), 404
            detail = {"url_id": url.id, "original_url": url.original_url}
            save_url_to_cache(short_code, detail)
            url_id = url.id
            orig_url = url.original_url
            cache_misses_total.inc()
        else:
            cache = json.loads(cache)
            logger.info(f"Its in cache key is {short_code}")
            url_id = cache["url_id"]
            orig_url = cache["original_url"]
            cache_hits_total.inc()
            
        add_to_queue(url_id)
        url_redirects_total.inc()
        return redirect(orig_url, code=302)
        
    finally:
        session.close()
