from flask import Blueprint, jsonify, request
from app.utils import get_short_code
from app.db import get_session
from app.models import URL

urls_bp = Blueprint("urls", __name__, url_prefix="/api/urls")

@urls_bp.route("", methods=["POST"])
def create_shortcode():

    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({
            "error": "URL is a required field"
        }), 400

    gen_short_code = get_short_code()
    session = get_session()
    try:
        url = URL(
            short_code = gen_short_code,
            original_url = data["url"],
        )
        session.add(url)
        session.commit()
        session.refresh(url)
        return jsonify({
            "short:code": url.short_code,
            "original_url": url.original_url,
            "created_at": url.created_at.isoformat()
        })
    except Exception as e:
        session.rollback()
        return jsonify({
            "error": str(e)
        }), 500
    finally:
        session.close()
