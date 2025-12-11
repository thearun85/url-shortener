from flask import Blueprint, jsonify, request
from app.db import get_session
from app.models import URL
from app.utils import get_short_code, validate_url, validate_short_code

urls_bp = Blueprint("URL", __name__, url_prefix="/api/urls")

MAX_RETRIES = 10

@urls_bp.route("", methods=['POST'])
def create_url():

    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({
            "error": "'url' is a required field"
        }), 400

    orig_url = data["url"]

    is_valid, error = validate_url(orig_url)
    if not is_valid:
        return jsonify({
            "error": error
        }), 400
        
    session = get_session()
    try:
        retries = 0
        while retries < MAX_RETRIES:
            gen_short_code = get_short_code()
            code = session.query(URL).filter_by(short_code=gen_short_code).first()
            if not code:
                break
            retries+=1

        if retries >= MAX_RETRIES:
            return jsonify({
                "error": "Failed to generate unique short code"
            }), 503
        url = URL(
            short_code = gen_short_code,
            original_url = orig_url,
        )
        session.add(url)
        session.commit()
        session.refresh(url)

        return jsonify({
            "short_code": url.short_code,
            "original_url": url.original_url,
            "created_at": url.created_at.isoformat(),
        }), 201
    except Exception as e:
        session.rollback()
        return jsonify({
            "error": str(e)
        }), 500
    finally:
        session.close()
    
@urls_bp.route("/<short_code>", methods=['GET'])
def get_url(short_code):

    is_valid, error = validate_short_code(short_code)
    if not is_valid:
        return jsonify({
            "error": error
        }), 400
        
    session = get_session()
    try:
        url = session.query(URL).filter_by(short_code=short_code).first()
        if not url:
            return jsonify({
                "error": "URL not found"
            }), 404

        click_count = len(url.clicks) if url.clicks else 0
        return jsonify({
            "short_code": url.short_code,
            "original_url": url.original_url,
            "created_at": url.created_at.isoformat(),
            "clicks": click_count,
        }), 200
    finally:
        session.close()
