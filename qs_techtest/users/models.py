"""User database models"""

import enum
import uuid
import re

from sqlalchemy.orm import validates
from sqlalchemy_utils import ChoiceType

from qs_techtest.extensions import db


EMAIL_REGEX = re.compile(r"[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,64}")


def generate_new_user_id():
    return str(uuid.uuid4())


class Country(enum.Enum):
    IRELAND = "Ireland"
    US = "United States"


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_new_user_id)
    first_name = db.Column(db.String(80), nullable=False, index=True)
    last_name = db.Column(db.String(80), nullable=False, index=True)
    email_address = db.Column(db.String(120), nullable=False, index=True)
    country = db.Column(ChoiceType(Country), nullable=True)

    @validates("email_address")
    def validate_email(self, key, value):
        match = EMAIL_REGEX.match(value)

        if match is None:
            raise AssertionError("Email does not match the required pattern.")

        return value

    @property
    def serialise(self):
        """Return object in json format"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "country": self.country.value or None,
        }

    def __repr__(self):
        """String representation"""
        return f"<User '{self.first_name} {self.last_name}'>"
