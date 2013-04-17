# Import SQLAlchemy ORM
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
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

		create_engine_string = '%s://%s:%s@%s/%s' % (engine_type, engine_user, engine_password, engine_host, engine_database)
		return create_engine_string


# Connect to Database
dbc = Database_creation()
engine = create_engine(dbc.create_engine_string(), echo=True)
Base = declarative_base()
	

# User
class User(Base):
	__tablename__ = "users"

	username = Column(String(32), primary_key=True)
	
	def __init__(self, username):
		self.username = username

# List
class List(Base):
	__tablename__ = "list"
	
	id = Column(Integer, primary_key=True)
	username = Column(String(32), ForeignKey("users.username"))
	list_title = Column(String(32))
	
	def __init__(self, username, list_title):
		self.username = username
		self.list_title = list_title
 
# Time event
class Time_event(Base):
	__tablename__ = "time_event"
	
	id = Column(Integer, primary_key=True)
	start_time = Column(Date)
	end_time = Column(Date)
	list_id = Column(Integer, ForeignKey("list.id"))

	def __init__(self, start_time, end_time, list_id):
		self.start_time = start_time
		self.end_time = end_time
		self.list_id = list_id

# Create tables above
Base.metadata.create_all(engine)
