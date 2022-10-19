from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.services.transaction_books_service import \
    create_transaction_books_service
from flask_jwt_extended import jwt_required

transaction_books_routes = Blueprint("transaction_books_routes", __name__)


@transaction_books_routes.route('/', methods=['POST'])
@jwt_required()
def create_transaction_books():
    data = request.get_json()
    return create_transaction_books_service(data)
