from flask import Blueprint, jsonify, redirect
from app.db import get_session
from app.models import URL, Click

redirect_bp = Blueprint("redirect", __name__)

@redirect_bp.route("/<short_code>", methods=["GET"])
def redirect_to_url(short_code):

    session = get_session()

    try:
        url = session.query(URL).filter_by(short_code=short_code).first()
        if not url:
            return jsonify({
                "erorr": "URL not found"
            }), 400
        click = Click(
            url_id = url.id,
        )
        session.add(click)
        session.commit()
        return redirect(url.original_url, code=302)
        
    finally:
        session.close()
