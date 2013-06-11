# Flask imports
from flask import Flask, request, render_template
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
# Database imports
# DB creation
from db.createdevdb import Database_creation
# SQL tables
from db.createdevdb import User, Customer_Information, Category, Tag, Category_Tag, Time_Event, Time_Tag
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# JSON import
from flask import json, jsonify

# Create the database engine
dbc = Database_creation()
engine = create_engine(dbc.create_engine_string(), echo=True)

app = Flask(__name__)

### BASIC SITE ###

# Index/home page
@app.route('/')
def index():
	return render_template('index.html')

### END BASIC SITE ###

### BEGIN AUTH SECTION ###

# Authorization - source: http://blog.luisrei.com/articles/flaskrest.html
def check_auth(username, password):
	# Check if the user is in the database
	Session = sessionmaker(bind=engine)
	session = Session()

	for user in session.query(User).filter_by(user_name=username): 
		return (user.user_name == username and check_password_hash(user.password, password))

# Return error for bad authentication or bad authorization
def auth_failure(failure_type):
	if failure_type == 'Authorization':
		message = {'message': "Requires Authorization"}
	if failure_type == 'Authenticate':
		message = {'message': "Requires Authentication"}
	
	resp = jsonify(message)
	resp.status_code = 401
	return resp

# Basic admin validation
def requires_admin(username, password):
	return (username == 'admin' and password == 'secret')

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		# No parameters passed in
		if not auth:
			return auth_failure(Authenicate)
		# Check if user passed in valid credentials
		elif not check_auth(auth.username, auth.password):
			return auth_failure(Authenticate)
		return f(*args, **kwargs)
	return decorated

# Check if user is requesting their own data
def check_privs(userid, username):
	Session = sessionmaker(bind=engine)
	session = Session()

	for user in session.query(User).filter_by(user_name=username):
		return (user.user_id == int(userid))	

### END AUTH SECTION ###

### BEGIN API ROUTES ###

# Get all users in the database
@app.route('/api/users/', methods = ['GET'])
@requires_auth
def db_users():
	Session = sessionmaker(bind=engine)
	session = Session()

	builder = []
	for user in session.query(Customer_Information).all():
		data = {'firstname':user.first_name,
			'lastname':user.last_name}
		builder.append(data)
	return jsonify(users=builder)

# Show Categories for a user
@app.route('/api/category/user/<userid>/', methods = ['GET'])
@requires_auth
def db_user_categories(userid):
	# Check if user is accessing their own data
	if check_privs(userid, request.authorization.username):
		Session = sessionmaker(bind=engine)
		session = Session()

		builder = []
		# All categories for a specific user
		for category in session.query(Category).filter_by(user_id=userid):
			data = {'category_name':category.category_name,
				'category_description':category.category_description}
			builder.append(data)
		return jsonify(categories=builder)
	# User doesnt have correct privileges
	return auth_failure(Authorize)

# Create user/password combo
@app.route('/api/user/login/', methods = ['POST'])
def db_user_pw():
	#TODO: Create this check as a decorator
	auth = request.authorization
	if not auth:
		auth_failure(Authenticate)
	else:
		if requires_admin(auth.username, auth.password):
			# Auth successful - Insert user into DB
			Session = sessionmaker(bind=engine)
			session = Session()
			
			# Mimic'ing a FORM
			new_username = request.form['username']
			new_pass = request.form['password']
			
			# Create the user object
			new_user = User(new_username, generate_password_hash(new_pass))
			# Save new user to the database
			session.add(new_user)
			session.flush()
			session.commit()
			
			# Creation successful
			resp = jsonify({'creation': "Successful"})
			resp.status_code = 200
			return resp
		else:
			auth_failure(Authorize)

# User specifics
@app.route('/api/user/<userid>/', methods = ['GET'])
@requires_auth
def db_user(userid):
	if check_privs(userid, request.authorization.username):
		Session = sessionmaker(bind=engine)
		session = Session()

		# Using 'get' because only fetching 1 row for a specific user	
		user = session.query(Customer_Information).get(userid)

		# Check if anything returned, if not 404
		if(user):
			return jsonify(user={'firstname':user.first_name, 'lastname':user.last_name, 'age':user.age, 'email':user.email, 'city':user.city, 'state':user.state, 'joined':str(user.date_joined)})
		else:
			return not_found() 
	return auth_failure(Authorize)

### END API ROUTES ### 

# Internal 404 to API
@app.errorhandler(404)
def not_found(error=None):
        message = {
                'status'        : 404,
                'message'       : 'Not Found: ' + request.url,
        }

        resp = jsonify(message)
        resp.status_code = 404

        return resp

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
	app.run()
