from api.utils.database import db
from api.utils.schema import ma
from marshmallow import fields
from datetime import datetime


class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    price = db.Column(db.Float, default=0.0)
    stock = db.Column(db.Integer, default=0)
    description = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, year, price, stock, description=str) -> None:
        self.title = title
        self.year = year
        self.price = price
        self.stock = stock
        self.description = description

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class BooksSchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = Books
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    year = fields.Integer(required=True)
    price = fields.Float()
    stock = fields.Integer()
    description = fields.String()
