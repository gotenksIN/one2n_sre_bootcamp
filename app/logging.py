import json
import logging
import time
import uuid
from datetime import datetime, timezone

from flask import g, has_app_context, request


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if has_app_context():
            try:
                if hasattr(g, "request_id"):
                    log_entry["request_id"] = g.request_id
            except RuntimeError:
                pass

        for key in (
            "method",
            "path",
            "status_code",
            "duration",
            "remote_addr",
            "user_agent",
            "route",
        ):
            value = getattr(record, key, None)
            if value is not None:
                log_entry[key] = value

        return json.dumps(log_entry)


def setup_logging(app):
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    @app.before_request
    def _assign_request_id():
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        g.request_start = time.time()

    @app.after_request
    def _log_request(response):
        duration = time.time() - g.pop("request_start", time.time())
        app.logger.info(
            "%s %s %s %.4fs",
            request.method,
            request.path,
            response.status_code,
            duration,
            extra={
                "method": request.method,
                "path": request.path,
                "status_code": str(response.status_code),
                "duration": f"{duration:.4f}",
                "remote_addr": request.remote_addr,
                "user_agent": request.headers.get("User-Agent", "-"),
                "route": request.endpoint,
            },
        )
        response.headers["X-Request-ID"] = g.pop("request_id", "")
        return response
