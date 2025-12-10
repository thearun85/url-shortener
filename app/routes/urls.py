from flask import Blueprint, jsonify, request
from app.db import get_session
from app.models import URL
from app.utils import get_short_code

urls_bp = Blueprint("URL", __name__, url_prefix="/api/urls")

MAX_RETRIES = 10

@urls_bp.route("", methods=['POST'])
def create_url():

    session = get_session()
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({
            "error": "'url' is a required field"
        }), 400

    orig_url = data["url"]

    gen_short_code = 'yry'
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
    
