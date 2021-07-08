from flask_testing import TestCase

from qs_techtest.app import create_app
from qs_techtest.extensions import db


class TestUsers(TestCase):

    def create_app(self):
        app = create_app("testing")
        self.client = app.test_client()
        return app

    def setUp(self) -> None:
        db.create_all()

    def test_add_user(self):
        request_payload = {
            "data": {
                "type": "users",
                "attributes": {
                    "first_name": "Foo",
                    "last_name": "Bar",
                    "email_address": "baz@qux.com",
                    "country": "Ireland",
                }
            }
        }

        response = self.client.post('/v1/users/', json=request_payload)

        self.assertEqual(200, response.status_code)

    def test_add_user_bad_email(self):
        request_payload = {
            "data": {
                "type": "users",
                "attributes": {
                    "first_name": "Foo",
                    "last_name": "Bar",
                    "email_address": "baz@qux.com",
                    "country": "Ireland",
                }
            }
        }

        response = self.client.post('/v1/users/', json=request_payload)

        self.assertEqual(500, response.status_code)

    def tearDown(self) -> None:
        db.drop_all()




