from flask import Flask

from .config import Config
from .extensions import db, migrate


def create_app(config_override=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_override:
        app.config.update(config_override)
    db.init_app(app)
    migrate.init_app(app, db)

    from .api.v1 import api_v1
    from .errors import register_error_handlers

    app.register_blueprint(api_v1)
    register_error_handlers(app)
    return app
