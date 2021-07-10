"""QS Tech Test application initialisation"""

from flask import Flask, make_response, jsonify

from qs_techtest import users
from qs_techtest.config import Development, Testing
from qs_techtest.extensions import db

# Import for register blueprints
import qs_techtest.users.views


configs = {
    "development": Development(),
    "testing": Testing(),
}


def create_app(app_env: str) -> Flask:
    """Creates the flask app and configures it"""
    app = Flask(__name__)
    app.config.from_object(configs[app_env])

    configure_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)

    return app


def configure_extensions(app: Flask) -> None:
    """Configures external extensions for flask app"""
    db.init_app(app)


def register_blueprints(app: Flask) -> None:
    """Registers blueprints from views modules"""
    app.register_blueprint(users.views.bp)


def register_error_handlers(app: Flask) -> None:
    """Registers bad request and internal server error handlers"""
    app.errorhandler(400)(bad_request)
    app.errorhandler(500)(server_error)


def bad_request(error):
    """Returns a JSON rep of the 400 bad request error"""
    return make_response(jsonify(error=error.description.message), 400)


def server_error(error):
    """Returns a JSON rep for the 500 internal server error"""
    db.session.rollback()
    return make_response(jsonify(error="Internal server error"), 500)
