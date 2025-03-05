from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired(), Length(min=2, max=50)])
    email_address = StringField(label="Email:", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password:", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label="Confirm Password:", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label="Create Account")

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! Please try a different username.")

    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError("Email already exists! Please try a different email.")

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")

class PurchaseItem(FlaskForm):
    submit = SubmitField(label="Buy")

class SellItem(FlaskForm):
    submit = SubmitField(label="Sell")
