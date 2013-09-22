import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime
import twilio.twiml

app = Flask(__name__)

client = MongoClient(os.environ['MONGOHQ_URL'])
db = client.get_default_database()
devices = db.devices

def update_device(name, msg):
	return devices.find_and_modify(
		query={'name': name},
		update={
			'name' : name,
			'msg' : msg,
			'time' : datetime.strftime(datetime.now(),'%a %b %d, %Y - %I:%M %p')
		},
		upsert=True
	)

def brace_handler(name, body):
	if body.startswith('{'):
		op = body.strip('{}').split(',')
		if op[0] == "bat":
			#TODO: update_device()
		if op[0] == "busy":
			#TODO: update_device()
	else:
		update_device(name, body)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		name = request.values.get('From', None)
		body = request.values.get('Body', None)
		sms_handler(name, body)

@app.route('/<name>', methods=['GET', 'POST'])
def profile(name):
	if request.method == 'POST':
		if len(request.form['msg'])>160:
			return 'fail: message > 160'
		else if name.startswith('+'):
			return 'fail: + reserved for SMS'
		else:
			brace_handler(name, request.form['msg'])
			return 'success'
	else:
		device = devices.find_one({'name' : name})
		return render_template('index.html', name=name, msg=device['msg'], time=device['time'])
