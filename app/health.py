from flask import Blueprint, current_app, jsonify
from sqlalchemy import text

from app.extensions import db

health_bp = Blueprint("health", __name__)


@health_bp.route("/health")
def health():
    """Platform-agnostic health check."""
    current_app.logger.debug("Health check requested")
    return jsonify({"status": "healthy"}), 200


@health_bp.route("/livez")
def livez():
    """Liveness check — process is alive."""
    return jsonify({"status": "alive"}), 200


@health_bp.route("/readyz")
def readyz():
    """Readiness check — database is reachable."""
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ready"}), 200
    except Exception:
        return jsonify({"status": "not ready"}), 503
