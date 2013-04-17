# Flask imports
from flask import Flask, request, render_template
from werkzeug.contrib.fixers import ProxyFix
# Database imports
from db.createdevdb import Time_event, User, List, Database_creation
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


# Show users
@app.route('/devapi/user/<userid>', methods = ['GET'])
def show_users(userid):
	users = {'1':'john', '2':'steve', '3':'bill', '4':'tony'}

        if userid in users:
                return jsonify({userid:users[userid]})
        else:
                return not_found()	

# Show users with SQL connection
@app.route('/devapi/sql/user')
def sql_show_users():
	Session = sessionmaker(bind=engine)
	session = Session()
	result = session.query(User).all()
	string_builder = ""
	for user in result:
		string_builder = string_builder + user.username
	return string_builder

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
