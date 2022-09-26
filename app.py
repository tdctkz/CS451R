from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from webforms import UserForm, LoginForm

# create a Flask instance
app = Flask(__name__)

# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fundraisers.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/donate_users'
# Secret key
app.config['SECRET_KEY'] = "donation"

# Initialize The database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

# create a route decorator
# Create Login pages
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Succesfull!!")
				return redirect(url_for('user_page'))
			else:
				flash("Wrong Password - Try Again!")
		else:
			flash("User Doesn't Exist!")
	return render_template('login.html', form=form)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged Out!")
	return redirect(url_for('login'))

# Create user Page
@app.route('/user_page', methods=['GET', 'POST'])
@login_required
def user_page():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":        
        name_to_update.fund_amount = request.form['fund_amount']
        try:
            db.session.commit()
            flash("Fund Amount Updated Successfully!")
            return render_template("user_page.html", form=form, name_to_update = name_to_update)
        except:
            flash("Error!  Looks like there was a problem...try again!")
            return render_template("user_page.html", form=form, name_to_update = name_to_update)
    else:
        return render_template("user_page.html", form=form, name_to_update = name_to_update, id=id)  


# Create  update pages
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):   
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html", form=form, name_to_update = name_to_update, id=id)
        except:
            flash("Error!  Looks like there was a problem...try again!")
            return render_template("update.html", form=form, name_to_update = name_to_update, id=id)
    else:       
        return render_template("update.html", form=form, name_to_update = name_to_update, id=id)        

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    if id == current_user.id:
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
    else:
        flash("Sorry, you can't delete that user! ")
        return redirect(url_for('user'))

# Create home page
@app.route('/')
def home():
    our_users = Users.query.order_by(Users.date_added)
    return render_template("home.html", our_users=our_users)

# Create Add user pages
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
   
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()

        if user:
            flash('Username already exists.')  
         
        else:            
            # Hash the password!!!
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")   
            user = Users(username=form.username.data, name=form.name.data,
            email=form.email.data, password_hash=hashed_pw, fund_amount = form.fund_amount.data)
            db.session.add(user)
            db.session.commit()        
            flash("User Added Successfully!")
        
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''        
        form.fund_amount.data = ''
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
		form=form,
		name=name,
		our_users=our_users)

# Create Custom Error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Create model
class Users(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    fund_amount = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
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