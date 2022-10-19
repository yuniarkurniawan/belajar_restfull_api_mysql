from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.users import Users, UsersSchema
from api.models.wallet import Wallet, WalletTransaction, \
    WalletSchema, WalletTransactionSchema
from api.utils.token import generate_verification_token, \
    confirm_verification_token
from api.utils.email import send_email
from flask import url_for, render_template_string, current_app
from api.utils.database import db
from flask_jwt_extended import create_access_token
from werkzeug.utils import secure_filename
import os


allowed_extensions = set(['image/jpeg', 'image/png', 'jpeg'])


def create_user_service(data):

    try:

        if Users.find_by_email(data['email']) or \
                Users.find_by_username(data['username']):
            return response_with(resp.USERNAME_EMAIL_ALREADY_EXIST_422)

        if len(data['card_id']) != 16:
            return response_with(resp.USERNAME_CARD_ID_INVALID_422)
        else:
            if Users.find_by_card_id(data['card_id']):
                return response_with(resp.USERNAME_CARD_ID_ALREADY_EXIST_422)
            else:
                tmp_birth_day = data['birth_day'].replace("/", "")
                tmp_list = list()
                tmp_list.append(tmp_birth_day[6:8])
                tmp_list.append(tmp_birth_day[4:6])
                tmp_list.append(tmp_birth_day[2:4])
                tmp_birth_day = ''.join(tmp_list)
                if data['card_id'][6:12] != tmp_birth_day:
                    return response_with(resp.USERNAME_CARD_ID_BIRTHDAY_422)

        data['password'] = Users.generate_hash(data['password'])
        user = Users(data['username'], data['password'], data['email'], data['card_id'], data['birth_day'])
        token = generate_verification_token(data['email'])
        verification_email = url_for('users_routes.verify_email',
                                     token=token,
                                     _external=True)
        html = render_template_string("<p>Selamat datang! Terima kasih Anda telah melakukan pendaftaran. \
                Silahkan klik link dibawah ini untuk aktifasi akun Anda:</p> <p> \
                <a href='{{ verification_email }}'>{{ verification_email }} \
                </a></p> <br> <p>Terima Kasih !</p>",
                                      verification_email=verification_email)
        subject = "Silahkan Verifikasi Akun Anda"
        send_email(user.email, subject, html)
        user.create()

        return response_with(resp.USER_CREATED_SUCCESS_201)

    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)


def verify_email_service(token=str):
    try:
        email = confirm_verification_token(token)
    except Exception as e:
        return response_with(resp.SERVER_ERROR_404)
    user = Users.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        return response_with(resp. INVALID_INPUT_422)
    else:
        user.is_verified = True
        db.session.add(user)

        # == BEGIN CREATE WALLET FOR THE 1ST TIME
        wallet = Wallet(user_id=user.id, wallet_name=user.username,
                        wallet_balance=0.0)
        # wallet_transaction = WalletTransaction(debit=0.0, credit=0.0)
        # wallet.wallettransactions.append(wallet_transaction)
        db.session.add(wallet)
        # db.session.add(wallet_transaction)
        # == END CREATE WALLET FOR THE 1ST TIME

        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={
                'message': 'E-mail terferikiasi, Anda dapat melakukan proses login.'
            })


def login_user_service(data):
    try:
        if data.get('email'):
            current_user = Users.find_by_email(data['email'])
        elif data.get('username'):
            current_user = Users.find_by_username(data['username'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if current_user and not current_user.is_verified:
            return response_with(resp.BAD_REQUEST_400)
        if Users.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(current_user.username)
            return response_with(
                resp.SUCCESS_201,
                value={
                    'message': 'Logged in as {}'.format(
                        current_user.username),
                    'access_token': access_token
                })
        return response_with(resp.UNAUTHORIZED_403)
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)


def allowed_file(filename):
    return filename in allowed_extensions


def update_avatar_service(user_id, file):
    try:
        get_user = Users.query.get_or_404(user_id)
        if file and allowed_file(file.content_type):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                      filename))
        get_user.avatar = url_for('uploaded_file',
                                    filename=filename,
                                    _external=True)
        db.session.add(get_user)
        db.session.commit()
        user_schema = UsersSchema()
        result = user_schema.dump(get_user)
        return response_with(resp.SUCCESS_200, value={"user": result})
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)
