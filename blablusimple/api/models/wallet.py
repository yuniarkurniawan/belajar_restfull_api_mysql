from api.utils.database import db
from api.utils.schema import ma
from marshmallow import fields
from datetime import datetime


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship("Users",)
    wallet_name = db.Column(db.String(255))
    wallet_balance = db.Column(db.Float)
    wallettransactions = \
        db.relationship('WalletTransaction',
                        backref='wallet', lazy=True)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)


class WalletTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'),
                          nullable=False)
    debit = db.Column(db.Float)
    credit = db.Column(db.Float)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class WalletTransactionSchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = WalletTransaction
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    debit = fields.Float()
    credit = fields.Float()


class WalletSchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = Wallet
        sqla_session = db.session

    id = fields.Int(dump_only=True)
    wallet_id = fields.Integer()
    wallet_name = fields.String()
    wallet_balance = fields.Float()
    wallettransactions = fields.Nested(WalletTransactionSchema, many=True)
