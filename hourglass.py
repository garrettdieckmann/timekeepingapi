# Flask imports
from flask import Flask, request, render_template
from werkzeug.contrib.fixers import ProxyFix
from werkzeug import check_password_hash
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

### DEV API ###

# Authorization - source: http://blog.luisrei.com/articles/flaskrest.html
def check_auth(username, password):
	# Check if the user is in the database
	Session = sessionmaker(bind=engine)
	session = Session()

	for user in session.query(User).filter_by(user_name=username): 
		if (user.user_name == username and user.password == check_password_hash(password)):
			return true
	return false

def authenticate():
	message = {'message': "Authenticate"}
	resp = jsonify(message)
	
	resp.status_code = 401
	return resp

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		# No parameters passed in
		if not auth:
			return authenticate()
		# Check if user passed in valid credentials
		elif not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated

# Root
@app.route('/devapi')
def devapi():
	return "Root of the dev api"

# New show users with SQL
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
def db_user_categories(userid):
	Session = sessionmaker(bind=engine)
	session = Session()

	builder = []
	# All categories for a specific user
	for category in session.query(Category).filter_by(user_id=userid):
		data = {'category_name':category.category_name,
			'category_description':category.category_description}
		builder.append(data)
	return jsonify(categories=builder)

# Return specifics about a particular user
@app.route('/api/user/<userid>/', methods = ['GET'])
def db_user(userid):
	Session = sessionmaker(bind=engine)
	session = Session()

	# Using 'get' because only fetching 1 row for a specific user	
	user = session.query(Customer_Information).get(userid)

	# Check if anything returned, if not 404
	if(user):
		return jsonify(user={'firstname':user.first_name, 'lastname':user.last_name, 'age':user.age, 'email':user.email, 'city':user.city, 'state':user.state, 'joined':str(user.date_joined)})
	else:
		return not_found() 

### END DEV API ###

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
