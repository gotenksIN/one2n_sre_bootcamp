from flask import current_app, jsonify
from sqlalchemy import text

from app.extensions import db

from . import api_v1


@api_v1.route('/healthcheck', methods=['GET'])
def healthcheck():
    """Get API health status."""
    current_app.logger.debug("Healthcheck requested")
    return jsonify({"status": "healthy"}), 200


@api_v1.route('/livez', methods=['GET'])
def livez():
    """Liveness check — process is alive."""
    return jsonify({"status": "alive"}), 200


@api_v1.route('/readyz', methods=['GET'])
def readyz():
    """Readiness check — database is reachable."""
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ready"}), 200
    except Exception:
        return jsonify({"status": "not ready"}), 503
