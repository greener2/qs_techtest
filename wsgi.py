import os

from qs_techtest.app import create_app


app = create_app(os.getenv("FLASK_ENV"))
