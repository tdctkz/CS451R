from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea
from flask_wtf.file import FileField

# Create a Log in form class
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

# Create a  user form class
class UserForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Your email", validators=[DataRequired()])
    address = StringField("address", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zipcode = IntegerField("Zip code", validators=[DataRequired()])
    donate_amount = IntegerField("Amount", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password= PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Posts Form
class FundraiserForm(FlaskForm):    
	title = StringField("Title", validators=[DataRequired()])
	description = StringField("Description", widget=TextArea())
	fundraiser_pic = FileField("Fundraiser Pic", validators=[DataRequired()])
	fund_goal = IntegerField("Fund Goal", validators=[DataRequired()])	
	submit = SubmitField("Submit")

#Create a donation form
class DonationForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired()])
    email = StringField("Your email", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zipcode = IntegerField("Zip code", validators=[DataRequired()])
    donate_amount = IntegerField("Amount", validators=[DataRequired()])