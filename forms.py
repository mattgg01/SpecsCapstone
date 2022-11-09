from flask_wtf import FlaskForm
from model import User
from wtforms import StringField,PasswordField,IntegerField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")

class OrderForm(FlaskForm):
    qty = IntegerField('How many cheeseburgers?', validators=[DataRequired()])
    submit = SubmitField('Place Order')

class UpdateOrder(FlaskForm):
    qty = IntegerField('')
    submit = SubmitField('Confirm Changes')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone',validators=[DataRequired()])
    newsletter = BooleanField('Receive monthly newsletters?')
    submit = SubmitField('Register!')



