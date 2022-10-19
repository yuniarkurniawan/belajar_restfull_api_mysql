import os
import logging
import sys
from flask import Flask, jsonify, send_from_directory
from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
from api.routes.users import users_routes
from api.routes.books import books_routes
from api.routes.wallet import wallet_routes
from api.routes.transaction_books import transaction_books_routes
from api.utils.email import mail
from flask_jwt_extended import JWTManager


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    jwt = JWTManager(app)
    mail.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(users_routes, url_prefix='/api/v1/users')
    app.register_blueprint(books_routes, url_prefix='/api/v1/books')
    app.register_blueprint(wallet_routes, url_prefix='/api/v1/wallet')
    app.register_blueprint(transaction_books_routes,
                           url_prefix='/api/v1/transaction_books')

    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)

    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp. SERVER_ERROR_404)

    jwt = JWTManager(app)
    mail.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
        level=logging.DEBUG)

    return app


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", use_reloader=False)
