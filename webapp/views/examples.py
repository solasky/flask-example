import os
import flask
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from webapp import app

# JSON (data type application/json)
@app.route('/API/example_json', methods=['GET', 'POST'])
def api_example_json():
	content = flask.request.get_json()
	return flask.jsonify(content)
# end def

# URL Query parameter
@app.route('/API/example_urlQuery', methods=['GET'])
def api_example_urlQuery():
	designation = flask.request.args.get('designation')
	username	= flask.request.args.get('username')
	template_html = 'example_urlQuery_echo.html'
	return flask.render_template(template_html, designation=designation, username=username)
# end def

# Form input
@app.route('/API/example_formInput', methods=['POST'])
def api_example_formInput():
	email	= flask.request.form.get('email')
	password = flask.request.form.get('password')
	template_html = 'example_formInput_echo.html'
	return flask.render_template(template_html, email=email, password=password)
# end def

# File upload
@app.route('/API/upload_file', methods=['POST'])
def upload():
	def allowed_file(filename):
		det_p = '.' in filename
		det_q = filename.split('.')[-1] in allowed_extensions
		return det_p & det_q
	# end def

	filename = None
	_file = flask.request.files['file']
	if _file and allowed_file(_file.filename):
		# Make the filename safe, remove unsupported chars
		filename = secure_filename(_file.filename)
		_file.save(os.path.join('/tmp', filename))
	# end if
	return flask.redirect(flask.url_for('uploaded_file', filename=filename))
# end def

@app.route('/API/uploaded/<filename>')
def uploaded_file(filename):
	if filename == None:
		return '<html>File not uploaded.</html>'
	else:
		return send_from_directory('/tmp', filename)
	# end if
# end def

