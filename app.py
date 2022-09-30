from email.policy import default
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from webforms import UserForm, LoginForm, DonationForm, FundraiserForm

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
@app.route('/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
      
		if user:
			# Check the hash
			if user.password == form.password.data:
				login_user(user)
				flash("Login Succesfull!!")
				return redirect(url_for('home'))
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
        name_to_update.goal_amount = request.form['goal_amount']
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
        name_to_update.password = request.form['password']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("user_page.html", form=form, name_to_update = name_to_update, id=id)
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
        form = UserForm()

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User Deleted Successfully!!")

            our_users = Users.query.order_by(Users.date_added)
            return render_template("login.html", 
                form=form,
                our_users=our_users)

        except:
            flash("Whoops! There was a problem deleting user, try again...")
            return render_template("login.html", 
                form=form, our_users=our_users)
    else:
        flash("Sorry, you can't delete that user! ")
        return redirect(url_for('user_page'))

# Create Add user pages
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
   
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()

        if user:
            flash('Username already exists.')  
        elif form.confirm_password.data != form.password.data:
            flash('Passwords must match!!Try again...')     
        else:                     
            user = Users(username=form.username.data, name=form.name.data,
            email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()        
            flash("User Added Successfully!")           
            return redirect(url_for('home'))
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password.data = ''      

    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
		form=form, our_users=our_users)

@app.route('/add_fundraiser', methods=['GET', 'POST'])
def add_fundraiser():
    form = FundraiserForm()
    
    if form.validate_on_submit():
        
        fundraiser = Fundraiser(title=form.title.data, description=form.description.data,
         fund_goal=form.fund_goal.data)
		# Clear The Form
        form.title.data = ''
        form.description.data = ''
        form.fund_goal.data = ''
        # form.slug.data = ''

		# Add post data to database
        db.session.add(fundraiser)
        db.session.commit()

		# Return a Message
        flash("A Fundraiser Created Successfully!")

	# Redirect to the webpage
    return render_template("add_fundraiser.html", form=form)

@app.route('/fundraiser/<int:id>')
def fundraiser(id):
    current_fundraiser = Fundraiser.query.get_or_404(id)
    return render_template("fundraiser_page.html", current_fundraiser=current_fundraiser)

@app.route('/fundraiser/delete/<int:id>')
@login_required
def delete_fundraiser(id):
	fundraiser_to_delete = Fundraiser.query.get_or_404(id)
	id = current_user.id
	if id == fundraiser_to_delete.id:
		try:
			db.session.delete(fundraiser_to_delete)
			db.session.commit()

			# Return a message
			flash("Fundraiser Was Deleted!")

			# Grab all the posts from the database
			all_fundraisers = Fundraiser.query.order_by(Fundraiser.date_created)
			return render_template("home.html", all_fundraisers=all_fundraisers)

		except:
			# Return an error message
			flash("Whoops! There was a problem deleting fundraiser, try again...")

			# Grab all the posts from the database
			all_fundraisers = Fundraiser.query.order_by(Fundraiser.date_created)
			return render_template("home.html", all_fundraisers=all_fundraisers)
	else:
		# Return a message
		flash("You Aren't Authorized To Delete the Fundraiser!")
		# Grab all the posts from the database
		all_fundraisers = Fundraiser.query.order_by(Fundraiser.date_created)
		return render_template("home.html", all_fundraisers=all_fundraisers)

# Create home page
@app.route('/home')
def home():
    all_fundraisers = Fundraiser.query.order_by(Fundraiser.date_created)
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
            flash("User fund Updated Successfully!")
            return redirect(url_for('home'))
        except:
            flash("Error!  Looks like there was a problem...try again!")
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
    fund_goal = db.Column(db.Integer)
    raised_amount = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)	

# Create Users model
class Users(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)        
    password = db.Column(db.String(128))   

    # Create A string
    def __repr__(self):
        return '<Name %r>' % self.name

if __name__ == '__main__':
    app.run(debug=True)