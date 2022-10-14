from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from webforms import UserForm, LoginForm, DonationForm, FundraiserForm
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import os
# create a Flask instance
app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'tdctkz142@gmail.com'
app.config['MAIL_PASSWORD'] = 'ghkoejyzodjyghll'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donation.db'

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
			# Checking user password
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				flash("Login Succesfull!!", 'success')
				return redirect(url_for('user_page'))
			else:
				flash("Wrong Password - Try Again!", 'danger')
		else:
			flash("User Doesn't Exist! Please create an account.", 'warning')
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
@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):   
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.password = generate_password_hash(request.form['password'], method='sha256')
        try:
            db.session.commit()
            flash("User Updated Successfully!", 'success')
            return render_template("user_page.html", form=form, name_to_update = name_to_update, id=id)
        except:
            flash("Error!  Looks like there was a problem...try again!", 'warning')
            return render_template("update_user.html", form=form, name_to_update = name_to_update, id=id)
    else:       
        return render_template("update_user.html", form=form, name_to_update = name_to_update, id=id) 

 # Create  update fundraiser
@app.route('/update_fundraiser/<int:id>', methods=['GET', 'POST'])
@login_required
def update_fundraiser(id):   
    form = FundraiserForm()
    fundraiser_to_update = Fundraiser.query.get_or_404(id)
    
    if request.method == "POST":
        fundraiser_to_update.title = request.form['title']
        fundraiser_to_update.description = request.form['description']
        fundraiser_to_update.fund_goal = request.form['fund_goal']        
        try:
            db.session.commit()
            flash("Fundraiser Updated Successfully!", 'success')
            return render_template("update_fundraiser.html", form=form, fundraiser_to_update = fundraiser_to_update, id=id)
        except:
            flash("Error!  Looks like there was a problem...try again!", 'warning')
            return render_template("update_fundraiser.html", form=form, fundraiser_to_update = fundraiser_to_update, id=id)
    else:       
        return render_template("update_fundraiser.html", form=form, fundraiser_to_update = fundraiser_to_update, id=id)         

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
            new_user = Users(username=form.username.data, name=form.name.data,
            email=form.email.data, password=generate_password_hash(form.password.data, method='sha256'))
            db.session.add(new_user)
            db.session.commit()        
            flash("User Added Successfully!", 'success')           
            form.name.data = ''
            form.username.data = ''
            form.email.data = ''
            form.password.data = ''     
            return redirect(url_for('login'))
       
    return render_template("add_user.html", form=form)

# Create a fundraiser form
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

# Create a Fundraiser individual view pages
@app.route('/fundraiser/<int:id>')
def fundraiser(id):
    current_fundraiser = Fundraiser.query.get_or_404(id)  
    donors = Donors.query.order_by(Donors.date_donated.desc())
    return render_template("fundraiser_page.html", current_fundraiser=current_fundraiser, donors=donors)

# Create function to delete a fundraiser
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

# Create forgot password function	
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = UserForm()   
    
    if request.method == "POST":
        user = Users.query.filter_by(email=form.email.data).first()
        if user: 
            flash("Check your email!! We sent an email that showing your password.", 'success')          
            msg = Message('Password Reset Request',
                  sender='tdctkz142@gmail.com',
                  recipients=[user.email])
            msg.body = f'''Here is your password:''' + user.password            
            mail.send(msg)
            return redirect(url_for('login'))
        else:
            flash("Email does not match in the system! Try again...", 'warning')
            
    return render_template("forgot_password.html", form=form)

# Create forgot username function	
@app.route('/forgot_username', methods=['GET', 'POST'])
def forgot_username():
    form = UserForm()    
   
    if request.method == "POST":
        user = Users.query.filter_by(email=form.email.data).first()
        if user: 
            flash("Check your email!! We sent an email that showing your username.", 'success') 
            msg = Message('Password Reset Request',
                  sender='tdctkz142@gmail.com',
                  recipients=[user.email])
            msg.body = f'''Here is your username:''' + user.username            
            mail.send(msg)
            return redirect(url_for('login'))
        else:
            flash("Email does not match in the system! Try again...", 'warning')
            
    return render_template("forgot_username.html", form=form)

# Create donation form page
@app.route('/donation/<int:id>', methods=['GET', 'POST'])
def donation(id):
    form = DonationForm()
    fund_to_update = Fundraiser.query.get_or_404(id) 
    dor = fund_to_update.id
    if request.method == "POST":
        fund_to_update.raised_amount += int(request.form['donate_amount'])   
        fund_to_update.current_process = round((fund_to_update.raised_amount / fund_to_update.fund_goal)*100)
        donor = Donors(fundraiser_id=dor, name=form.name.data, email=form.email.data,
         address=form.address.data, city=form.city.data, state=form.state.data, zipcode=form.zipcode.data,
         donate_amount=form.donate_amount.data)
        try:
            db.session.add(donor)
            db.session.commit()
            form.donate_amount.data = ''
            flash("Fundraiser's fund Updated Successfully!", 'success')
            return redirect(url_for('home'))
        except:
            flash("Error!  Looks like there was a problem...try again!", 'warning')
            return render_template("donation_form.html", form=form, fund_to_update = fund_to_update)
    else:       
        return render_template("donation_form.html", form=form, fund_to_update = fund_to_update, id=id)        

# Create Custom Error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
   
# Database creation
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

     # Fundraiser Can Have Many donors 
    donor = db.relationship('Donors', backref='dor')
    
# Create Donors model
class Donors(db.Model): 
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(100), nullable=False)    
    email = db.Column(db.String(200), nullable=False)
    date_donated = db.Column(db.DateTime, default=datetime.utcnow)        
    donate_amount = db.Column(db.Integer)
    address = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    # Foreign Key To Link Fundraiser (refer to primary key of the fundraiser)
    fundraiser_id = db.Column(db.Integer, db.ForeignKey('fundraiser.id'))    

# Create Users model
class Users(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(300), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)        
    password = db.Column(db.String(128)) 
    
    # User Can Have Many Fundraisers 
    fundraiser = db.relationship('Fundraiser', backref='funder')    
    
    def __repr__(self):
        return '<Name %r>' % self.name

class AdminViews(ModelView):
    def is_accessible(self):
         return current_user.is_authenticated and current_user.username == "admin"

    def inaccessible_callback(self, name, **kwargs):        
        return redirect(url_for('login'))

admin = Admin(app)
# Create admin views management
admin.add_view(AdminViews(Users, db.session))
admin.add_view(AdminViews(Fundraiser, db.session))
admin.add_view(AdminViews(Donors, db.session))

if __name__ == '__main__':
    app.run(debug=True)