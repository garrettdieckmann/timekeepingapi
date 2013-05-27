# Flask imports
from flask import Flask, request, render_template
from werkzeug.contrib.fixers import ProxyFix
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

# Root
@app.route('/devapi')
def devapi():
	return "Root of the dev api"

# New show users with SQL
@app.route('/api/users/', methods = ['GET'])
def db_users():
	Session = sessionmaker(bind=engine)
	session = Session()

	builder = ''
	for user in session.query(Customer_Information).all():	
		builder = builder + '{firstname:' + user.first_name + '},' 
	builder = builder[:-1]
	return builder

# Return specifics about a particular user
@app.route('/api/user/<userid>/', methods = ['GET'])
def db_user(userid):
	Session = sessionmaker(bind=engine)
	session = Session()

	# Using 'get' because only fetching 1 row for a specific user	
	user = session.query(Customer_Information).get(userid)

	# Check if anything returned, if not 404
	if(user):
		return jsonify({'firstname':user.first_name, 'lastname':user.last_name, 'age':user.age, 'email':user.email, 'city':user.city, 'state':user.state, 'joined':str(user.date_joined)})
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
