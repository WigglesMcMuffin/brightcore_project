from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_app import config
import pyjade

#from flask_app.database import db.session

db = SQLAlchemy()

def create_app(env=None, debug=False):
	app = Flask(__name__)
	app.debug = debug
	
	app = Flask(__name__)
	app.config['SECRET_KEY'] =  'britecore_secret'
	app.config['SQLALCHEMY_DATABASE_URI'] = config.get_database_uri(env)
	app.debug = debug
	app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
	
	db.init_app(app)
	
	return app

import flask_app.views
