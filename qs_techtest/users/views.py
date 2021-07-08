from flask import Blueprint, request, make_response, jsonify
from flask_expects_json import expects_json

from qs_techtest.extensions import db
from qs_techtest.users.models import User
from qs_techtest.users.schemas import add_user_schema

bp = Blueprint("users", __name__, url_prefix="/v1/users")


@bp.post("/")
@expects_json(add_user_schema)
def add_user():
    request_data = request.json

    user_attrs = request_data["data"]["attributes"]

    try:
        new_user = User(
            first_name=user_attrs["first_name"],
            last_name=user_attrs["last_name"],
            email_address=user_attrs["email_address"],
            country=user_attrs.get("country", None),
        )
        db.session.add(new_user)
        db.session.commit()
    except AssertionError as e:
        return make_response(jsonify(error=str(e)), 400)

    return make_response(user_attrs, 200)
