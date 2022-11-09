from flask import Flask, render_template, request, flash, session, redirect, url_for, abort
from model import connect_to_db, db, User, load_user, login_manager, Orders
from forms import LoginForm, RegistrationForm, OrderForm, UpdateOrder, DeleteOrder
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

##End of Boiler

#Home 
@app.route("/home")
def home():
    """View homepage."""
    print(current_user)
    return render_template("home.html")

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


#Welcome users
@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')


@app.route('/order_track', methods=['GET','PUT','DELETE'])
@login_required
def order_track():
    updateform = UpdateOrder()
    deleteform = DeleteOrder()
    orders = Orders.query.filter_by(cust_id=current_user.id)
    if updateform.validate_on_submit():
        orders = Orders.query.filter_by(cust_id=current_user.id)
        

    return render_template('order_track.html', deleteform=deleteform, orders=orders, updateform=updateform)



#LATE NIGHT STUFF PROBABLY WON'T USE. IF YOU DONT USE MOVE update_order back to order_track function
@app.route('/update_order/<order_id>', methods=['POST'])
def update_order(order_id):
    update_order = UpdateOrder()
    order = Orders.query.get(order_id)
    if update_order.validate_on_submit():
        order.qty = update_order.qty.data
        db.session.add(order)
        db.session.commit()
    return redirect(url_for('order_track'))

@app.route('/delete_order/<order_id>', methods=['POST'])
def delete_order(order_id):
    delete_order = DeleteOrder()
    order = Orders.query.get(order_id)
    if delete_order.validate_on_submit():
        db.session.delete(order)
        db.session.commit()
    return redirect(url_for('order_track'))



#Logout users
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
        if user.check_password(form.password.data) == True:
            login_user(user)
            flash('Logged in successfully!')
            print("Password is correct")
            return redirect(url_for('home'))

        else:
            print("Incorrect password")

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('home')
                

            return redirect(next)

    return render_template('login.html',form=form)
    

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    address=form.address.data,
                    phone=form.phone.data,
                    newsletter=form.newsletter.data
                    )
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering!")
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/order',methods=['GET','POST'])
def order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Orders(qty=form.qty.data,
                    cust_id=current_user.id
                    )
        db.session.add(order)
        db.session.commit()
        flash("Thanks for ordering!")
        return redirect(url_for('order_track'))
    return render_template('order.html',form=form)





if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)
