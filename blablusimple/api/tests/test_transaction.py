import json
from api.utils.test_base import BaseTestCase
from api.models.books import Books
from api.models.users import Users
from api.models.wallet import Wallet, WalletTransaction
from flask_jwt_extended import create_access_token
from api.utils.database import db


def create_wallet():
    user1 = Users(email="your_email",
                  username='your_username',
                  password=Users.generate_hash('your_password'),
                  card_id="your_id_card",
                  birth_day="YYYY/MM/DD",
                  is_verified=True).create()

    wallet = Wallet(user_id=user1.id,
                    wallet_name=user1.username,
                    wallet_balance=10000000)
    wallet_transaction = WalletTransaction(debit=10000000, credit=0)
    wallet.wallettransactions.append(wallet_transaction)
    db.session.add(wallet)
    db.session.add(wallet_transaction)

    db.session.commit()


def login():
    access_token = \
        create_access_token(identity='your_email')
    return access_token


class TestTransaction(BaseTestCase):
    def setUp(self):
        super(TestTransaction, self).setUp()
        create_wallet()

    def test_create_transaction(self):

        book_1 = Books(title='KKN Di Desa Penari',
                   year=2020,
                   price=1000,
                   stock=90,
                   description='Novel horor fiksi').create()

        book_2 = Books(title='The Origin',
                       year=2020,
                       price=1000,
                       stock=50,
                       description='Novel fiksi ilmiah').create()

        token = login()
        data_transaction = {
            "user_id":1,
            "description":"Beli buku baru",
            "books":[
                {
                    "id":1,
                    "total":2
                },
                {
                    "id":2,
                    "total":1
                }
            ]
        }
        response = self.app.post(
            '/api/v1/transaction_books/',
            data=json.dumps(data_transaction),
            content_type='application/json',
            headers={'Authorization': 'Bearer '+token}
        )

        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('success' in data['code'])


    def test_create_transaction_wallet_less_than(self):

        book_1 = Books(title='KKN Di Desa Penari',
                   year=2020,
                   price=100000000,
                   stock=90,
                   description='Novel horor fiksi').create()
        book_2 = Books(title='The Origin',
                       year=2020,
                       price=500000000,
                       stock=50,
                       description='Novel fiksi ilmiah').create()


        token = login()
        data_transaction = {
            "user_id":1,
            "description":"Beli buku baru",
            "books":[
                {
                    "id":1,
                    "total":1
                },
                {
                    "id":2,
                    "total":2
                }
            ]
        }
        response = self.app.post(
            '/api/v1/transaction_books/',
            data=json.dumps(data_transaction),
            content_type='application/json',
            headers={'Authorization': 'Bearer '+token}
        )

        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)
        self.assertTrue('invalidInput' in data['code'])

if __name__ == '__main__':
    unittest.main()