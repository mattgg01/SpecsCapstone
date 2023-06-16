from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import RegistrationForm,LoginForm,DeleteOrder,OrderForm,BurgerForm
from model import User, Order, connect_to_db,db,Burger
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Flask-Login user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Homepage
@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    """View homepage."""
    print(current_user)
    return render_template("home.html")

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

# Welcome page for authenticated users
@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

# Page to view and manage orders
@app.route('/order_track', methods=['GET','PUT','DELETE'])
@login_required
def order_track():
    deleteform = DeleteOrder()
    orders = Order.query.filter_by(customer_id=current_user.customer_id)

    return render_template('order_track.html', deleteform=deleteform, orders=orders)


# Delete order API
@app.route('/delete_order/<order_id>', methods=['POST'])
def delete_order(order_id):
    delete_order_form = DeleteOrder()
    order = Order.query.get(order_id)
    if delete_order_form.validate_on_submit():
        db.session.delete(order)
        db.session.commit()
    return redirect(url_for('order_track'))

# Logout API
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('home'))
    
#login users
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

#register users
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    address=form.address.data,
                    phone=form.phone.data,
                    newsletter=form.newsletter.data,
                    )
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering!")
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/order', methods=['GET', 'POST'])
def order():
    form = OrderForm()
    if form.validate_on_submit():
        # create order
        order = Order(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            quantity_burgers=form.quantity_burgers.data,
            quantity_drinks=form.quantity_drinks.data,
            delivery_address=form.delivery_address.data
        )
        db.session.add(order)
        db.session.commit()
        
        # create burgers for order
        for burger_form in form.burgers.entries:
            burger_data = burger_form.data
            cheese = burger_data.get('cheese', False)
            tomatoes = burger_data.get('tomatoes', False)
            lettuce = burger_data.get('lettuce', False)
            onion = burger_data.get('onion', False)
            bacon = burger_data.get('bacon', False)
            ketchup = burger_data.get('ketchup', False)
            
            if cheese or tomatoes or lettuce or onion or bacon or ketchup:
                burger = Burger(
                    cheese=cheese,
                    tomatoes=tomatoes,
                    lettuce=lettuce,
                    onion=onion,
                    bacon=bacon,
                    ketchup=ketchup,
                    order=order
                )
                db.session.add(burger)
                db.session.commit()

        flash('Your order has been submitted!', 'success')
        return redirect(url_for('home'))
    return render_template('order.html', title='Order', form=form)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)
