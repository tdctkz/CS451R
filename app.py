from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from webforms import UserForm, LoginForm, DonationForm, FundraiserForm
from werkzeug.utils import secure_filename
import os
# create a Flask instance
app = Flask(__name__)

# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/donate_users'
# Secret key
app.config['SECRET_KEY'] = "donation"

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# image requirements
# limit upload size upto 8mb
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = {'jpg', 'jpeg','png','JPG','JPEG','PNG'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
			if user.password == form.password.data:
				login_user(user)
				flash("Login Succesfull!!", 'success')
				return redirect(url_for('user_page'))
			else:
				flash("Wrong Password - Try Again!", 'danger')
		else:
			flash("User Doesn't Exist!", 'warning')
	return render_template('login.html', form=form)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged Out!", 'success')
	return redirect(url_for('login'))

# Create user Page
@app.route('/user_page', methods=['GET', 'POST'])
@login_required
def user_page():   
    user_fundraisers = Fundraiser.query.order_by(Fundraiser.date_created.desc())    
    return render_template("user_page.html", user_fundraisers=user_fundraisers)

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
        name_to_update.password = request.form['password']
        try:
            db.session.commit()
            flash("User Updated Successfully!", 'success')
            return render_template("user_page.html", form=form, name_to_update = name_to_update, id=id)
        except:
            flash("Error!  Looks like there was a problem...try again!", 'warning')
            return render_template("update.html", form=form, name_to_update = name_to_update, id=id)
    else:       
        return render_template("update.html", form=form, name_to_update = name_to_update, id=id)        


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    if id == current_user.id:
        user_to_delete = Users.query.get_or_404(id)
        form = UserForm()

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User Deleted Successfully!!", 'success')

            our_users = Users.query.order_by(Users.date_added)
            return render_template("login.html", 
                form=form,
                our_users=our_users)

        except:
            flash("Whoops! There was a problem deleting user, try again...", 'warning')
            return render_template("login.html", 
                form=form, our_users=our_users)
    else:
        flash("Sorry, you can't delete that user! ", 'danger')
        return redirect(url_for('user_page'))

# Create Add user pages
@app.route('/sign-up', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
   
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()

        if user:
            flash('Username already exists.', 'warning')  
        elif form.confirm_password.data != form.password.data:
            flash('Passwords must match!!Try again...', 'warning')     
        else:                     
            user = Users(username=form.username.data, name=form.name.data,
            email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()        
            flash("User Added Successfully!", 'success')           
            return redirect(url_for('home'))
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password.data = ''      

    our_users = Users.query.order_by(Users.date_added)    
    return render_template("add_user.html", 
		form=form, our_users=our_users)

@app.route('/create_fundraiser', methods=['GET', 'POST'])
def create_fundraiser():
    form = FundraiserForm()
    
    if form.validate_on_submit():
        f = request.files['fundraiser_pic']
        if allowed_file(f.filename):
            file = secure_filename(f.filename)
            funder = current_user.id
            fundraiser = Fundraiser(user_id=funder, title=form.title.data, description=form.description.data,
            fund_goal=form.fund_goal.data, fundraiser_pic=file)
        else:
            flash("Your file must be in type of 'jpg', 'jpeg','png'!!", 'warning')
            return render_template("create_fundraiser.html", form=form)
		# Clear The Form
        form.title.data = ''
        form.description.data = ''
        form.fund_goal.data = ''
        
        
		# Add post data to database
        db.session.add(fundraiser)
        db.session.commit()
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
		# Return a Message
        flash("A Fundraiser Created Successfully!", 'success')
        return redirect(url_for('user_page'))
	# Redirect to the webpage
    return render_template("create_fundraiser.html", form=form)

@app.route('/fundraiser/<int:id>')
def fundraiser(id):
    current_fundraiser = Fundraiser.query.get_or_404(id)
    current_fundraiser.current_process = round((current_fundraiser.raised_amount / current_fundraiser.fund_goal)*100)
    return render_template("fundraiser_page.html", current_fundraiser=current_fundraiser)

@app.route('/fundraiser/delete/<int:id>')
@login_required
def delete_fundraiser(id):
	fundraiser_to_delete = Fundraiser.query.get_or_404(id)
	id = current_user.id
	if id == fundraiser_to_delete.user_id:
		try:
			db.session.delete(fundraiser_to_delete)
			db.session.commit()

			# Return a message
			flash("Fundraiser Was Deleted!", 'success')			
			return render_template("user_page.html")

		except:
			# Return an error message
			flash("Whoops! There was a problem deleting fundraiser, try again...", 'warning')
			return render_template("user_page.html")
	else:
		# Return a message
		flash("You Aren't Authorized To Delete the Fundraiser!", 'danger')		
		return render_template("user_page.html")

# Create home page
@app.route('/')
def home():
    all_fundraisers = Fundraiser.query.order_by(Fundraiser.date_created.desc())
    return render_template("home.html", all_fundraisers=all_fundraisers)


# @app.route('/reset_password', methods=['GET', 'POST'])
# def reset_password():
#     form = UserForm()
#     change_password = Users.query.get_or_404(id)
    
#     if request.method == "POST":
#         user = Users.query.filter_by(email=form.email.data).first()
#         if user:        
#             flash('Check your email!! We sent an email to reset your password.') 
#             return redirect(url_for('login'))
#         else:
#             flash('Email does not match in the system! Try again...')
            
#     return render_template("reset_password.html", form=form)

@app.route('/donation/<int:id>', methods=['GET', 'POST'])
def donation(id):
    form = DonationForm()
    fund_to_update = Fundraiser.query.get_or_404(id)
    
    if request.method == "POST":
        fund_to_update.raised_amount += int(request.form['amount'])
        try:
            db.session.commit()
            flash("User fund Updated Successfully!", 'success')
            return redirect(url_for('home'))
        except:
            flash("Error!  Looks like there was a problem...try again!", 'warning')
            return render_template("donation_form.html", form=form, fund_to_update = fund_to_update, id=id)
    else:       
        return render_template("donation_form.html", form=form, fund_to_update = fund_to_update, id=id)        

# Create Custom Error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Create a Fundraser  model
class Fundraiser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    fundraiser_pic = db.Column(db.String(), nullable=True)
    fund_goal = db.Column(db.Integer)
    raised_amount = db.Column(db.Integer, default=0)
    current_process = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)	
    # Foreign Key To Link Users (refer to primary key of the user)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# class Donors(db.Model): 
#     id = db.Column(db.Integer, primary_key=True)   
#     name = db.Column(db.String(200), nullable=False)    
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     date_donated = db.Column(db.DateTime, default=datetime.utcnow)        
    
    # Donor Can Have Many donation 
    #fundraiser = db.relationship('Fundraiser', backref='funder')

# Create Users model
class Users(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)        
    password = db.Column(db.String(128))   
    # User Can Have Many Posts 
    fundraiser = db.relationship('Fundraiser', backref='funder')
    
    def __repr__(self):
        return '<Name %r>' % self.name

if __name__ == '__main__':
    app.run(debug=True)