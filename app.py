from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# create a Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "donation"


# Create a form class
class NameForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

# create a route decorator
# Create Login pages
@app.route('/')

def login():
    return render_template("login.html")

# Create Sign up pages
@app.route('/sign_up')

def sign_up():
    return render_template("sign_up.html")

# Create Name pages
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    # Validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template("name.html", name=name, form=form)

# Create Custom Error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", 404)

