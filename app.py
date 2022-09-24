from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash 

# create a Flask instance
app = Flask(__name__)

# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donateUsers.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/donate_users'
# Secret key
app.config['SECRET_KEY'] = "donation"

# Initialize The database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create model
class Users(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #color = db.Column(db.String(120))
    # Do some password stuff!
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create A string
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a form class
class NameForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a form class
class UserForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired()])
    #color = StringField("Color")
    email = StringField("Your email", validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
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

# Create Add user pages
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
  
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password!!!
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        #form.color.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
		form=form,
		name=name,
		our_users=our_users)

# Create  update pages
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):   
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        #name_to_update.color = request.form['color']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html", form=form, name_to_update = name_to_update)
        except:
            flash("Error!  Looks like there was a problem...try again!")
            return render_template("update.html", form=form, name_to_update = name_to_update)
    else:
        flash("User Updated Successfully!")
        return render_template("update.html", form=form, name_to_update = name_to_update)        

@app.route('/delete/<int:id>')
def delete(id):
	user_to_delete = Users.query.get_or_404(id)
	name = None
	form = UserForm()

	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User Deleted Successfully!!")

		our_users = Users.query.order_by(Users.date_added)
		return render_template("add_user.html", 
			form=form,
			name=name,
			our_users=our_users)

	except:
		flash("Whoops! There was a problem deleting user, try again...")
		return render_template("add_user.html", 
			form=form, name=name,our_users=our_users)
	

# Create home page
@app.route('/home')
def home():
    our_users = Users.query.order_by(Users.date_added)
    return render_template("home.html", our_users=our_users)

# Create Name pages
@app.route('/Dashboard', methods=['GET', 'POST'])
def Dashboard():
    name = None
    form = NameForm()
    # Validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Summited")
    return render_template("Dashboard.html",
        name=name, 
        form=form)

# Create Custom Error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", 404)

