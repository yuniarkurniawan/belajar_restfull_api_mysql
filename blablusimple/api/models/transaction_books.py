from api.utils.database import db
from api.utils.schema import ma
from marshmallow import fields
from datetime import datetime
from api.models.books import BooksSchema


class TransactionBooks(db.Model):
    __tablename__ = 'transaction_books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship("Users",)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_number = db.Column(db.String(20), nullable=False)
    sequence_number = db.Column(db.Integer(), default=0)
    description = db.Column(db.String(255))
    details = db.relationship("TransactionBookDetails")

    def __init__(self, user_id, description, sequence_number, transaction_number=str()):
        self.user_id = user_id
        self.description = description
        self.sequence_number = sequence_number
        self.transaction_number = transaction_number


class TransactionBookDetails(db.Model):
    __tablename__ = 'transaction_books_detail'

    transaction_id = db.Column(db.Integer(),
                               db.ForeignKey('transaction_books.id'),
                               primary_key=True)
    book_id = db.Column(db.Integer(), db.ForeignKey('books.id'),
                        primary_key=True)
    book_price = db.Column(db.Float, default=0.0)
    total_buy = db.Column(db.Integer, default=0)
    total_price = db.Column(db.Float, default=0.0)
    description = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    book = db.relationship('Books')


class TransactionBookDetailsSchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = TransactionBookDetails
        sqla_session = db.session

    book_price = fields.Float()
    total_buy = fields.Integer()
    total_price = fields.Float()
    book = fields.Nested(BooksSchema,
                         many=False,
                         only=['title', 'year', 'description'])


class TransactionBooksSchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = TransactionBooks
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    transaction_number = fields.String()
    description = fields.String()
    details = fields.Nested(TransactionBookDetailsSchema, many=True)
