from api.utils.database import db
from api.utils.schema import ma
from marshmallow import fields
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    card_id = db.Column(db.String(16), unique=True, nullable=False)
    birth_day = db.Column(db.Date, nullable=False)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, email, card_id, birth_day,
                 is_verified=False) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.card_id = card_id
        self.birth_day = datetime.strptime(birth_day, '%Y/%m/%d').date()
        self.is_verified = is_verified

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_card_id(cls, card_id):
        return cls.query.filter_by(card_id=card_id).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UsersSchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = Users
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    card_id = fields.String(required=True)
    #birth_day = fields.Date()
