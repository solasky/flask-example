import os
import sys
import flask
from flask import Flask, redirect, url_for
from webapp.database import init_db, db_session
from webapp.models.models import ContentClassificationTask

import inspect
curdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
app = Flask(__name__.split('.')[0], template_folder=curdir+'/templates')
app.config['DEBUG'] = True
init_db()

#########################
######### VIEWS #########
#########################
@app.route('/')
def root():
	return redirect(url_for('index'))
# end def

@app.route('/index.html', methods=('GET',))
def index():
	return flask.render_template('index.html')
# end def

@app.route('/example_input.html')
def example():
	template_html = 'example_input.html'
	return flask.render_template(template_html)
# end def

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

from .views.examples import *
from .views.tasktable import *
########### END #########
