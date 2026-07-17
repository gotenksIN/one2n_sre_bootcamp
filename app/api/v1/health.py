from flask import current_app, jsonify

from . import api_v1


@api_v1.route('/healthcheck', methods=['GET'])
def healthcheck():
    """Get API health status."""
    current_app.logger.debug("Healthcheck requested")
    return jsonify({"status": "healthy"}), 200
