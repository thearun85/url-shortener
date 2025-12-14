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
        }), 201
    except Exception as e:
        session.rollback()
        return jsonify({
            "error": str(e)
        }), 500
    finally:
        session.close()

@urls_bp.route("/<short_code>", methods=["GET"])
def get_url(short_code):

    session = get_session()

    try:
        url = session.query(URL).filter_by(short_code=short_code).first()
        if not url:
            return jsonify({
                "error": "URL not found"
            }), 400
        click_count = len(url.clicks) if url.clicks else 0
        return jsonify({
            "short_code": url.short_code,
            "original_url": url.original_url,
            "created_at": url.created_at.isoformat(),
            "clicks": click_count,
        }), 200

    finally:
        session.close()
