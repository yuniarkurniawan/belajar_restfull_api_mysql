from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.books import Books, BooksSchema
from flask_jwt_extended import jwt_required
from api.services.wallet_service import top_up_wallet_service, \
    get_wallet_user_service
from flask_jwt_extended import jwt_required


wallet_routes = Blueprint("wallet_routes", __name__)


@wallet_routes.route('/topup', methods=['POST'])
def top_up_wallet_user():
    data = request.get_json()
    return top_up_wallet_service(data)


@wallet_routes.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_wallet_user(user_id):
    return get_wallet_user_service(user_id)
