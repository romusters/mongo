#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect
import flask
import flask.ext.login as flask_login
import sys
from pymongo import MongoClient
import logging
# from crossd import crossdomain
from flask.ext.cors import CORS, cross_origin

import mongo

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

m = mongo.mongo()


app = Flask(__name__)

handle = m.db

app.secret_key = 'abcdef'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


users = {'robert': {'pw': 'secret'}, 'anton': {'pw': 'secret'}}

class User(flask_login.UserMixin):
	pass


@login_manager.user_loader
def user_loader(email):
	if email not in users:
		return

	user = User()
	user.id = email
	return user


@login_manager.request_loader
def request_loader(request):
	email = request.form.get('email')
	if email not in users:
		return

	user = User()
	user.id = email

	user.is_authenticated = request.form['pw'] == users[email]['pw']

	return user

@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return '''
			   <form action='login' method='POST'>
				<input type='text' name='email' id='email' placeholder='email'></input>
				<input type='password' name='pw' id='pw' placeholder='password'></input>
				<input type='submit' name='submit'></input>
			   </form>
			   '''

	email = flask.request.form['email']
	if flask.request.form['pw'] == users[email]['pw']:
		user = User()
		user.id = email
		flask_login.login_user(user)
		return flask.redirect(flask.url_for('protected'))

	return 'Bad login'



@app.route('/protected')
@flask_login.login_required
def protected():
	return '''
			<html>
				<head>
					<meta http-equiv="refresh" content="1;url=/index" />
				</head>
				<body>
					<h1>Logged in. Redirecting...</h1>
				</body>
			</html>
		'''

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return 'Logged out'

@login_manager.unauthorized_handler

def unauthorized_handler():
	return 'Unauthorized'


# Bind our index page to both www.domain.com
@app.route("/index", methods=['GET'])
@flask_login.login_required
def index():
	userinputs = [x for x in handle.mycollection.find()]
	logger.info(flask.ext.login.current_user.id)
	return render_template('index.html', userinputs=userinputs)

@app.route("/annotation", methods=['GET'])
def annotation():
	d = {"a": flask.ext.login.current_user.id}
	return flask.jsonify(d)

@app.route("/label", methods=['POST'])
def label():
	user = flask.ext.login.current_user.id

	data = request.get_json()

	id = '5728b6b1c3dc0b196a3128db'

	logger.info(user)
	logger.info(data['agreement'])
	logger.info(data['label'])

	m.addlabel(id, user, data['label'])
	m.addagreement(id, user, data['agreement'])

	return "200"

@app.route("/write", methods=['POST'])
def write():
	userinput = request.form.get("userinput")
	oid = handle.mycollection.insert({"message":userinput})
	return redirect ("/index")



if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5002)

