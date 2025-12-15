from flask import Blueprint, jsonify, redirect
from app.db import get_session
from app.models import URL
from app.utils import validate_shortcode, url_redirects_total
from app.queue import add_to_queue

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
        url = session.query(URL).filter_by(short_code=short_code).first()
        if not url:
            return jsonify({
                "erorr": "URL not found"
            }), 404
        add_to_queue(url.id)
        url_redirects_total.inc()
        return redirect(url.original_url, code=302)
        
    finally:
        session.close()
