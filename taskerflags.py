import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime
import twilio.twiml

app = Flask(__name__)

client = MongoClient(os.environ['MONGOHQ_URL'])
db = client.get_default_database()
devices = db.devices

## Device object
# ID   - used for url, when accessed via SMS this is the phone number
# msg  - short informational message
# time - timestamp of last update
# bat  - current battery status. 0 for critical, 1 for feelin' fine
# busy - current google calendar busy status. 0 for available, 1 for busy

def update_device(ID, msg, **kwargs):
	if 
	return devices.find_and_modify(
		query={'ID': ID},
		update={
			'ID' : ID,
			'msg' : msg,
			'time' : datetime.strftime(datetime.now(),'%a %b %d, %Y - %I:%M %p')
		},
		upsert=True
	)

def brace_handler(ID, body):
	if body.startswith('{'):
		op = body.strip('{}').split(',')
		if op[0] == "bat":
			#TODO: update_device()
		if op[0] == "busy":
			#TODO: update_device()
	else:
		update_device(ID, body)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		ID = request.values.get('From', None)
		body = request.values.get('Body', None)
		sms_handler(ID, body)

@app.route('/<ID>', methods=['GET', 'POST'])
def profile(ID):
	if request.method == 'POST':
		if len(request.form['msg'])>160:
			return 'fail: message > 160'
		else if ID.startswith('+'):
			return 'fail: + reserved for SMS'
		else:
			brace_handler(ID, request.form['msg'])
			return 'success'
	else:
		device = devices.find_one({'ID' : ID})
		return render_template('index.html', ID=ID, msg=device['msg'], time=device['time'])
