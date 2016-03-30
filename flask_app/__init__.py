from flask import Flask
import pyjade

from flask_app.database import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] =  'brightcore_secret'
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

import flask_app.views

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
