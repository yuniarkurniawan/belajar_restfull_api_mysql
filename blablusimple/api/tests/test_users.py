import json
from api.utils.test_base import BaseTestCase
from api.models.users import Users
from datetime import datetime


def create_users():

    user1 = Users(email="your_email",
                  username='your_username',
                  password=Users.generate_hash('your_password'),
                  card_id="your_id_card",
                  birth_day="YYYY/MM/DD",
                  is_verified=True).create()

    user2 = Users(email="your_email",
                  username='your_username',
                  card_id="your_id_card",
                  birth_day="YYYY/MM/DD",
                  password=Users.generate_hash('your_password')).create()


class TestUsers(BaseTestCase):
    def setUp(self):
        super(TestUsers, self).setUp()
        create_users()

    def test_create_users(self):

        user = {
          "username": "your_username",
          "password": "your_password",
          "email": "your_email",
          "card_id": "your_id_card",
          "birth_day": "YYYY/MM/DD"
        }
        response = self.app.post(
            '/api/v1/users/',
            data=json.dumps(user),
            content_type='application/json'
        )

        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('success' in data['code'])

    def test_create_users_without_username(self):

        user = {
          "password": "your_password",
          "email": "your_email"
        }
        response = self.app.post(
            '/api/v1/users/',
            data=json.dumps(user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)

    def test_create_users_without_email(self):

        user = {
          "password": "your_password",
          "username": "your_username"
        }
        response = self.app.post(
            '/api/v1/users/',
            data=json.dumps(user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)

    def test_login_unverified(self):
        # email dan password tidak sama dengan data pada fungsi create_users
        user = {
          "email": "your_email",
          "password": "your_password"
        }

        response = self.app.post(
            '/api/v1/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )

        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)

    def test_login_user_wrong_credentianls(self):

        user = {
          "email": "your_email",
          "password": "your_password"
        }

        response = self.app.post(
            '/api/v1/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )

        data = json.loads(response.data)
        self.assertEqual(403, response.status_code)

    def test_login_user_true_credentianls(self):

        user = {
          "email": "your_email",
          "password": "your_password"
        }

        response = self.app.post(
            '/api/v1/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )

        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('access_token' in data)


if __name__ == '__main__':
    unittest.main()
