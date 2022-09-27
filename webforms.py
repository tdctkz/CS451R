from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

# Create a Log in form class
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")


# Create a  user form class
class UserForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired(), Length(min=2, max=20)])
    fund_amount = StringField("Your goal", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Your email", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password= PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

