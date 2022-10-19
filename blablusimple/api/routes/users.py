from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.users import Users, UsersSchema
from api.services.users_service import create_user_service,\
    verify_email_service, login_user_service, update_avatar_service


users_routes = Blueprint("users_routes", __name__)


@users_routes.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    return create_user_service(data)


@users_routes.route('/confirm/<token>', methods=['GET'])
def verify_email(token):
    return verify_email_service(token)


@users_routes.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    return login_user_service(data)


@users_routes.route('/avatar/<int:user_id>', methods=['POST'])
def update_user_avatar(user_id):
    file = request.files['avatar']
    return update_avatar_service(user_id, file)
