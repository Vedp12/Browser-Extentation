import os

from flask import Flask

from config import Config
from app.extensions import db


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize database
    db.init_app(app)

    # Register models with SQLAlchemy
    from app.models import URLmodal, NOTEmodal, QRmodal

    # Register blueprints
    from app.routes.web import web
    from app.routes.api import api

    app.register_blueprint(web)
    app.register_blueprint(api)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app