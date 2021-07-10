"""Testing User endpoints"""

from flask_testing import TestCase

from qs_techtest.app import create_app
from qs_techtest.extensions import db
from qs_techtest.users.models import User


class TestUsers(TestCase):
    """Testing user endpoints"""

    def create_app(self):
        """Creates a test app and a test client."""

        app = create_app("testing")
        self.client = app.test_client()
        return app

    def setUp(self) -> None:
        """Sets up the database for the test and populates some test data."""

        db.create_all()
        user1 = User(
            first_name="James",
            last_name="Bond",
            email_address="james.bond@mi6.co.uk",
            country="United States"
        )
        user2 = User(
            first_name="Aaron",
            last_name="Zodiac",
            email_address="azod@gmail.com",
            country="Ireland",
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def test_add_user(self):
        """Tests the add user endpoint with a valid payload."""

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

    def test_add_user_invalid_email(self):
        """Tests the add user endpoint with an invalid email (checks email regex validation"""

        request_payload = {
            "data": {
                "type": "users",
                "attributes": {
                    "first_name": "Foo",
                    "last_name": "Bar",
                    "email_address": "bazqux.com",
                    "country": "Ireland",
                }
            }
        }

        response = self.client.post('/v1/users/', json=request_payload)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Email does not match the required pattern.", response.json["error"])

    def test_add_user_invalid_country(self):
        """Tests user endpoint with invalid country field (checks ChoiceType validation)"""

        request_payload = {
            "data": {
                "type": "users",
                "attributes": {
                    "first_name": "Foo",
                    "last_name": "Bar",
                    "email_address": "baz@qux.com",
                    "country": "England",
                }
            }
        }

        response = self.client.post('/v1/users/', json=request_payload)

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            f"{request_payload['data']['attributes']['country']!r} is not a valid country, please choose either "
            f"'Ireland' or 'United States'",
            response.json["error"]
        )

    def test_add_user_missing_first_name(self):
        """Tests add user endpoint with missing first_name field (checks jsonschema validation)"""

        request_payload = {
            "data": {
                "type": "users",
                "attributes": {
                    "last_name": "Bar",
                    "email_address": "baz@qux.com",
                    "country": "Ireland",
                }
            }
        }

        response = self.client.post('/v1/users/', json=request_payload)

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            "'first_name' is a required property",
            response.json["error"]
        )

    def test_add_user_missing_last_name(self):
        """Tests add user endpoint with missing last_name field (checks jsonschema validation)"""

        request_payload = {
            "data": {
                "type": "users",
                "attributes": {
                    "first_name": "Foo",
                    "email_address": "baz@qux.com",
                    "country": "Ireland",
                }
            }
        }

        response = self.client.post('/v1/users/', json=request_payload)

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            "'last_name' is a required property",
            response.json["error"]
        )

    def test_add_user_missing_email(self):
        """Tests add user endpoint with missing email_address field (checks jsonschema validation)"""

        request_payload = {
            "data": {
                "type": "users",
                "attributes": {
                    "first_name": "Foo",
                    "last_name": "Bar",
                    "country": "England",
                }
            }
        }

        response = self.client.post('/v1/users/', json=request_payload)

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            "'email_address' is a required property",
            response.json["error"]
        )

    def test_add_user_missing_country(self):
        """Tests add user endpoint with missing country field (checks jsonschema validation)"""

        request_payload = {
            "data": {
                "type": "users",
                "attributes": {
                    "first_name": "Foo",
                    "last_name": "Bar",
                    "email_address": "baz@qux.com",
                }
            }
        }

        response = self.client.post('/v1/users/', json=request_payload)

        self.assertEqual(200, response.status_code)

    def test_get_users(self):
        """Tests get users"""

        response = self.client.get('/v1/users/')

        data = response.json

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(data))
        # Default sorting is first name in descending order, so J comes first
        self.assertEqual("James", data[0]["first_name"])
        self.assertEqual("Bond", data[0]["last_name"])
        self.assertEqual("james.bond@mi6.co.uk", data[0]["email_address"])
        self.assertEqual("United States", data[0]["country"])
        self.assertEqual("Aaron", data[1]["first_name"])
        self.assertEqual("Zodiac", data[1]["last_name"])
        self.assertEqual("azod@gmail.com", data[1]["email_address"])
        self.assertEqual("Ireland", data[1]["country"])

    def test_get_users_sort_last_name(self):
        """Tests get users endpoint with sort on last name"""

        response = self.client.get('/v1/users/?sort=last_name')

        data = response.json

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(data))
        # Sorting now is last_name in descending order, so Z comes first
        self.assertEqual("Aaron", data[0]["first_name"])
        self.assertEqual("Zodiac", data[0]["last_name"])
        self.assertEqual("azod@gmail.com", data[0]["email_address"])
        self.assertEqual("Ireland", data[0]["country"])
        self.assertEqual("James", data[1]["first_name"])
        self.assertEqual("Bond", data[1]["last_name"])
        self.assertEqual("james.bond@mi6.co.uk", data[1]["email_address"])
        self.assertEqual("United States", data[1]["country"])

    def tearDown(self) -> None:
        """Tidies up test database"""

        db.drop_all()
