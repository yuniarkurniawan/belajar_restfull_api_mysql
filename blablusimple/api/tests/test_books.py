import json
from api.utils.test_base import BaseTestCase
from api.models.books import Books
from flask_jwt_extended import create_access_token


def create_books():

    book_1 = Books(title='KKN Di Desa Penari',
                   year=2020,
                   price=10000,
                   stock=90,
                   description='Novel horor fiksi').create()
    book_2 = Books(title='The Origin',
                   year=2020,
                   price=10000,
                   stock=90,
                   description='Novel fiksi ilmiah').create()


def login():
    access_token = \
        create_access_token(identity='<your_email>')
    return access_token


class TestBooks(BaseTestCase):
    def setUp(self):
        super(TestBooks, self).setUp()
        create_books()

    def test_get_books_list(self):
        token = login()
        response = self.app.get(
            '/api/v1/books/?page=1&per_page=10&search=kkn',
            content_type='application/json',
            headers={'Authorization': 'Bearer '+token}
        )

        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('data' in data)

    def test_get_books_list_over_page(self):
        token = login()
        response = self.app.get(
            '/api/v1/books/?page=100&per_page=10&search=kkn',
            content_type='application/json',
            headers={'Authorization': 'Bearer '+token}
        )

        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertTrue('data' in data)


if __name__ == '__main__':
    unittest.main()
