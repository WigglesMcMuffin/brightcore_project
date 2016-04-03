from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask_app import config

import pyjade

db = SQLAlchemy()
csrf = CsrfProtect()

def create_app(env=None, debug=False, testing=False):
    app = Flask(__name__)
    app.debug = debug

    app = Flask(__name__)
    app.config['SECRET_KEY'] =  'britecore_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_database_uri(env)
    app.debug = debug
    app.config['TESTING'] = testing
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

    db.init_app(app)
    csrf.init_app(app)

    from flask_app.views.main import main_site
    from flask_app.views.forms import form_endpoints
    app.register_blueprint(main_site)
    app.register_blueprint(form_endpoints)

    return app
