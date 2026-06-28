from flask import Flask
from flask_migrate import Migrate

from .config import Config
from .models import db

migrate = Migrate()

def create_app(config_override=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_override:
        app.config.update(config_override)
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import init_routes
    init_routes(app)
    return app
