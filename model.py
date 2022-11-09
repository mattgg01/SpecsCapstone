import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


app = Flask(__name__)
db = SQLAlchemy()
Migrate(app,db)


class User(db.Model,UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    first_name = db.Column(db.String(35))
    last_name = db.Column(db.String(55))
    address = db.Column(db.String(90))
    phone = db.Column(db.String)
    newsletter = db.Column(db.Boolean)

    def __init__(self, email, password, first_name, last_name, address, phone, newsletter):
        self.email = email
        self.password_hash = password ##Add password hasher later
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.newsletter = newsletter

    def check_password(self,password):
        if self.password_hash == password:
            return True
        else:
            return False


    def __repr__(self):
        return f"<User user_id={self.id} email={self.email} first_name={self.first_name} last_name={self.last_name} phone={self.phone} address={self.address} newsletter={self.newsletter}>"

class Orders(db.Model):
    __tablename__ = "orders"
    cust_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    qty = db.Column(db.Integer)
  

    def __init__(self, qty, cust_id, ):
        self.cust_id = cust_id
        self.qty = qty
        

    def __repr__(self):
        return f'Charboiled Burgers,\n Qty: {self.qty} \n Order ID: {self.order_id}'

class Drinks():
    __tablename__ = "drinks"


    drink_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    drink_name = db.Column(db.String(20))
    price = db.Column(db.Float)

    def __init__(self, drink_name, price):
        self.drink_name = drink_name
        self.price = price

    def __repr__(self):
        return f"<Drink drink_name={self.drink_name} drink_id={self.drink_id} price={self.price}"





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