from flask import Flask

from qs_techtest import users
from qs_techtest.config import Development, Testing
from qs_techtest.extensions import db, migrate

# Import for flask-migrate to work
import qs_techtest.users.models

# Import for register blueprints
import qs_techtest.users.views


configs = {
    "development": Development(),
    "testing": Testing(),
}


def create_app(app_env: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(configs[app_env])

    configure_extensions(app)
    register_blueprints(app)

    return app


def configure_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(users.views.bp)
