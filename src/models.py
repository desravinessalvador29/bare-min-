from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.String(20), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=True)

    def __repr__(self):
        return '<Product %r>' % self.username
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
        }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    state = db.Column(db.String(80), unique=False, nullable=False)
    country = db.Column(db.String(80), unique=False, nullable=False)
    zip_code = db.Column(db.Integer, unique=False, nullable=False)
    card_number = db.Column(db.String(120), unique=True, nullable=False)
    card_expiration_date = db.Column(db.String(80), unique=False, nullable=False)
    card_cvv = db.Column(db.Integer, unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=True)

    def __repr__(self):
        return '<Order %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "product_id": self.product_id,
            "created_date": self.created_date
        }