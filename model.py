import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

login_manager = LoginManager()

@login_manager.user_loader
def load_user(customer_id):
    return User.query.get(customer_id)


app = Flask(__name__)
db = SQLAlchemy()
Migrate(app,db)

class User(UserMixin, db.Model):
    __tablename__ = 'customers'

    def get_id(self):
        return str(self.customer_id)
    customer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    newsletter = db.Column(db.Boolean, nullable=False, default=False)
    orders = db.relationship('Order', primaryjoin='User.customer_id == Order.customer_id', backref='customers')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Customer {self.email}>'


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    quantity_burgers = db.Column(db.Integer, nullable=False)
    quantity_drinks = db.Column(db.Integer, nullable=False)
    delivery_address = db.Column(db.String(240), nullable=False)
    burgers = db.relationship('Burger', backref='orders', lazy=True)

class Burger(db.Model):
    __tablename__ = "burgers"
    burger_id = db.Column(db.Integer, primary_key=True)
    cheese = db.Column(db.Boolean, nullable=False)
    tomatoes = db.Column(db.Boolean, nullable=False)
    lettuce = db.Column(db.Boolean, nullable=False)
    onion = db.Column(db.Boolean, nullable=False)
    bacon = db.Column(db.Boolean, nullable=False)
    ketchup = db.Column(db.Boolean, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)



def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")