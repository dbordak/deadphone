import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime
import twilio.twiml

app = Flask(__name__)

client = MongoClient(os.environ['MONGOHQ_URL'])
db = client.get_default_database()
devices = db.devices

@app.route('/', methods=['POST'])
def sms_handler():
	name = request.values.get('From', None)
	body = request.values.get('Body', None)

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

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<name>', methods=['GET', 'POST'])
def profile(name):
	if request.method == 'POST':
		if len(request.form['msg'])>160:
			return 'fail: message > 160'
		else:
			update_device(name, request.form['msg'])
			return 'success'
	else:
		device = devices.find_one({'name' : name})
		return render_template('index.html', name=name, msg=device['msg'], time=device['time'])
