from flask import Blueprint, jsonify, Response
from app.utils import get_metrics

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
    })

@health_bp.route("/metrics")
def metrics():
    data, content_type = get_metrics()
    return Response(data, mimetype=content_type)
