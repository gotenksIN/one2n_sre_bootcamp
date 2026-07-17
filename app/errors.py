from flask import jsonify
from werkzeug.exceptions import HTTPException

from .extensions import db


class AppError(Exception):
    status_code = 500


class ValidationError(AppError):
    status_code = 400


class NotFoundError(AppError):
    status_code = 404


def handle_validation_error(error):
    return jsonify({"error": str(error)}), 400


def handle_not_found_error(error):
    return jsonify({"error": str(error)}), 404


def handle_app_error(error):
    return jsonify({"error": str(error)}), error.status_code


def handle_unexpected_error(error):
    if isinstance(error, HTTPException):
        response = jsonify(
            {"error": error.description or "Internal server error"}
        )
        response.status_code = error.code
        return response
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500


def register_error_handlers(app):
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(NotFoundError, handle_not_found_error)
    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(Exception, handle_unexpected_error)
