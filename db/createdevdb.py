# Import SQLAlchemy ORM
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
# Import password hasing
from werkzeug.security import generate_password_hash
# Import config parser
import ConfigParser
import os.path

class Database_creation():
	def create_engine_string(self):
		# Get DB params from config file
		db_config = ConfigParser.ConfigParser()
		if (os.path.isfile("dbconfig.ini")):
			db_config.read("dbconfig.ini")
		else:
			db_config.read("db/dbconfig.ini")

		# Parms for create_engine
		engine_type = db_config.get("database","type")
		engine_user = db_config.get("database","user")
		engine_password = db_config.get("database","password")
		engine_host = db_config.get("database","host")
		engine_database = db_config.get("database","database")

		create_engine_string = '%s://%s:%s@%s/%s' % (engine_type, 
			engine_user, engine_password, engine_host, engine_database)
		return create_engine_string


# Connect to Database
dbc = Database_creation()
engine = create_engine(dbc.create_engine_string(), echo=False)
Base = declarative_base()
	

# User
class User(Base):
	__tablename__ = "users"

	user_id = Column(Integer, primary_key = True)
	user_name = Column(String(32))
	password = Column(String(64))
	
	def __init__(self, user_name, password):
		self.user_name = user_name
		# hash the password passed in
		self.password = generate_password_hash(password)

# Customer Information: Name, Age, Email Address, Time Zone, City, State, Zip Code
class Customer_Information(Base):
	__tablename__ = "customer_information"
	
	user_id = Column(Integer, primary_key = True)
	first_name = Column(String(32))
	last_name = Column(String(32))
	age = Column(Integer)
	gender = Column(Boolean, unique=False, default=True) #0 - Male, 1 - Female
	email = Column(String(128))
	time_zone = Column(String(32))
	zipcode = Column(Integer)
	city = Column(String(32))
	state = Column(String(32))
	date_joined = Column(Date) #date the user signed up for the app
	
	def __init__(self, user_id, first_name, last_name, age, gender, email, time_zone, zipcode, city, state, date_joined):
		self.user_id = user_id
		self.first_name = first_name
		self.last_name = last_name
		self.age = age
		self.gender = gender
		self.email = email
		self.time_zone = time_zone
		self.zipcode = zipcode
		self.city = city
		self.state = state
		self.date_joined = date_joined
 
# Category
class Category(Base):
	__tablename__ = "category"
	
	category_id = Column(Integer, primary_key=True)
	category_name = Column(String(64))
	category_description = Column(String(32))
	user_id = Column(Integer, ForeignKey("users.user_id"))

	def __init__(self, category_name, category_description, user_id):
		self.category_name = category_name
		self.category_description = category_description
		self.user_id = user_id

		
# Tab
class Tag(Base):
	__tablename__ = "tag"
	
	tag_id = Column(Integer, primary_key=True)
	tag_name = Column(String(64))
	tag_description = Column(String(32))

	def __init__(self, tag_name, tag_description):
		self.tag_name = tag_name
		self.tag_description = tag_description

		
# Category-Tab Table
class Category_Tag(Base):
	__tablename__ = "category_tag"
	
	id = Column(Integer, primary_key=True)
	category_id = Column(Integer, ForeignKey("category.category_id"))
	tag_id = Column(Integer, ForeignKey("tag.tag_id"))

	def __init__(self, category_id, tag_id):
		self.category_id = category_id
		self.tag_id = tag_id
		
		
# Time event
class Time_Event(Base):
	__tablename__ = "time_event"
	
	time_id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.user_id"))
	start_time = Column(Date) # Should be timestamp
	end_time = Column(Date) # Should be timestamp
	

	def __init__(self, user_id, start_time, end_time):
		self.user_id = user_id
		self.start_time = start_time
		self.end_time = end_time
		
# Category-Tab Table
class Time_Tag(Base):
	__tablename__ = "time_tag"
	
	id = Column(Integer, primary_key=True)
	time_id = Column(Integer, ForeignKey("time_event.time_id"))
	tag_id = Column(Integer, ForeignKey("tag.tag_id"))

	def __init__(self, time_id, tag_id):
		self.time_id = time_id
		self.tag_id = tag_id

# Create tables above
Base.metadata.create_all(engine)
