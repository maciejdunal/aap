from . import db
from flask_login import UserMixin
from datetime import datetime, timezone

class Watch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    image_url = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(10), nullable=False)  # male/female
    category = db.Column(db.String(50), nullable=False)  # sport/luxury

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('watch.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    watch = db.relationship('Watch', backref='cart_items')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # Poprawione dla SQLAlchemy 2.0
    total_price = db.Column(db.Float, nullable=False)

    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('watch.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    watch = db.relationship('Watch', backref='order_items')
