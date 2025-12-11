from flask import Blueprint, jsonify, redirect
from app.db import get_session
from app.models import URL, Click
from app.utils import validate_short_code, redirects_total

redirect_bp = Blueprint("redirect", __name__)

@redirect_bp.route("/<short_code>")
def redirect_to_url(short_code):
    is_valid, error = validate_short_code(short_code)
    print(f"short code is {short_code}")
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
        click = Click(
            url_id = url.id,
        )
        session.add(click)
        session.commit()
        redirects_total.inc()
        return redirect(url.original_url, code=302)
    finally:
        session.close()
