from flask import Blueprint, jsonify, redirect
from app.db import get_session
from app.models import URL

redirect_bp = Blueprint("redirect", __name__)

@redirect_bp.route("/<short_code>")
def redirect_to_url(short_code):

    session = get_session()
    try:
        url = session.query(URL).filter_by(short_code=short_code).first()
        if not url:
            return jsonify({
                "error": "URL not found"
            }), 404
        return redirect(url.original_url, code=302)
    finally:
        session.close()
