from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.books import Books, BooksSchema
from api.services.books_service import books_list_service
from flask_jwt_extended import jwt_required

books_routes = Blueprint("books_routes", __name__)


@books_routes.route('/', methods=['GET'])
@jwt_required()
def get_books_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    search = request.args.get('search', type=str)
    return books_list_service(page, per_page, search)
