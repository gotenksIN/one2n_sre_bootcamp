from flask import Flask

from .config import Config
from .extensions import db, metrics, migrate


def create_app(config_override=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_override:
        app.config.update(config_override)

    if not app.config.get("TESTING"):
        if not app.config.get("SQLALCHEMY_DATABASE_URI"):
            raise RuntimeError("DATABASE_URL must be set")
        if not app.config.get("SECRET_KEY"):
            raise RuntimeError("SECRET_KEY must be set")

    db.init_app(app)
    migrate.init_app(app, db)
    metrics.init_app(app)

    from .api.v1 import api_v1
    from .errors import register_error_handlers
    from .health import health_bp
    from .logging import setup_logging

    setup_logging(app)
    app.register_blueprint(health_bp)
    app.register_blueprint(api_v1)
    register_error_handlers(app)
    return app
