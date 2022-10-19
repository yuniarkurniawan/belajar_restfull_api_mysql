import json
from api.utils.test_base import BaseTestCase
from api.models.wallet import Wallet, WalletTransaction
from api.models.users import Users
from api.utils.database import db
from flask_jwt_extended import create_access_token
from datetime import datetime


def update_wallet():
    user1 = Users(email="your_email",
                  username='your_username',
                  password=Users.generate_hash('your_password'),
                  card_id="your_id_card",
                  birth_day="YYYY/MM/DD",
                  is_verified=True).create()

    wallet = Wallet(user_id=user1.id,
                    wallet_name=user1.username,
                    wallet_balance=0)
    db.session.add(wallet)
    db.session.commit()


def login():
    access_token = \
        create_access_token(identity='your_email')
    return access_token


class TestWallet(BaseTestCase):
    def setUp(self):
        super(TestWallet, self).setUp()
        update_wallet()

    def test_create_top_up(self):
        data_topup = {
              "user_id": 1,
              "top_up": 40000
            }

        response = self.app.post(
            '/api/v1/wallet/topup',
            data=json.dumps(data_topup),
            content_type='application/json'
        )

        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('success' in data['code'])

    def test_create_zero_top_up(self):
        data_topup = {
              "user_id": 1,
              "top_up": 0
            }

        response = self.app.post(
            '/api/v1/wallet/topup',
            data=json.dumps(data_topup),
            content_type='application/json'
        )

        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)
        self.assertTrue('invalidInput' in data['code'])

    def test_get_wallet_user(self):
        token = login()
        response = self.app.get(
            '/api/v1/wallet/user/1',
            content_type='application/json',
            headers={'Authorization': 'Bearer '+token}
        )

        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('success' in data['code'])


# if __name__ == '__main__':
#     unittest.main()
