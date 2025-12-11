from flask import Blueprint, jsonify
from app.utils import get_metrics

health_bp = Blueprint("health", __name__)

@health_bp.route("/health")
def health_check():
    return jsonify({
        "status": "healthy"
    }), 200

@health_bp.route("/metrics")
def metrics():
    return jsonify(get_metrics()), 200
