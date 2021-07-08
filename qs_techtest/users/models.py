import enum
import uuid
import re

from sqlalchemy.orm import validates

from qs_techtest.extensions import db


EMAIL_REGEX = re.compile(r"[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,64}")


def generate_new_user_id():
    return str(uuid.uuid4())


class Countries(enum.Enum):
    IRELAND = "Ireland"
    US = "United States"


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_new_user_id)
    first_name = db.Column(db.String(80), nullable=False, index=True)
    last_name = db.Column(db.String(80), nullable=False, index=True)
    email_address = db.Column(db.String(120), nullable=False, index=True)
    country = db.Column(db.Enum(Countries), nullable=True)

    @validates("email_address")
    def validate_email(self, key, value):
        match = EMAIL_REGEX.match(value)

        if match is None:
            raise AssertionError("Email does not match the required pattern.")

        return value
