from flask_wtf import FlaskForm
from model import User
from wtforms import StringField,PasswordField,IntegerField,SubmitField,FieldList,FormField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")

class BurgerForm(FlaskForm):
    cheese = BooleanField('Cheese')
    tomatoes = BooleanField('Tomatoes')
    lettuce = BooleanField('Lettuce')
    onion = BooleanField('Onion')
    bacon = BooleanField('Bacon')
    ketchup = BooleanField('Ketchup')

class OrderForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    quantity_burgers = IntegerField('Number of Burgers', validators=[DataRequired()])
    quantity_drinks = IntegerField('Number of Drinks', validators=[DataRequired()])
    delivery_address = StringField('Delivery Address', validators=[DataRequired()])
    burgers = FieldList(FormField(BurgerForm), min_entries=1)
    add_burger = SubmitField('Add Burger')
    submit = SubmitField('Submit Order')

class DeleteOrder(FlaskForm):
    submit = SubmitField('Delete Order')

class RegistrationForm(FlaskForm):
    def validate_email(self, email):
        existing_email = User.query.filter_by(
            email=email.data).first()
        if existing_email:
            raise ValidationError(
                "That email is already in use"
            )
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    newsletter = BooleanField('Subscribe to Newsletter')
    submit = SubmitField("Register!")