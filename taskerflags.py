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
	device = {
		'ID' : ID,
		'time' : datetime.strftime(datetime.now(),'%a %b %d, %Y - %I:%M %p')
	}
	if len(kwargs):
		if kwargs.keys()[0] == 'bat':
			device['bat']=kwargs['bat']
		if kwargs.keys()[0] == 'busy':
			device['busy']=kwargs['busy']
		if kwargs.keys()[0] == 'name':
			device['name']=kwargs['name']
	else:
		device['msg']=msg
	return devices.find_and_modify(
		query={'ID': ID},
		update=device,
		upsert=True
	)

def brace_handler(ID, body):
	if body.startswith('{'):
		opt = body.strip('{}').split(',')
		if opt[0] == "bat":
			update_device(ID, body, bat=opt[1])
		if opt[0] == "busy":
			update_device(ID, body, busy=opt[1])
		if opt[0] == "name":
			update_device(ID, body, name=opt[1])
	else:
		update_device(ID, body)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		ID = request.values.get('From', None)
		body = request.values.get('Body', None)
		brace_handler(ID, body)

@app.route('/<ID>', methods=['GET', 'POST'])
def profile(ID):
	if request.method == 'POST':
		if len(request.form['msg'])>160:
			return 'fail: message > 160'
		elif ID.startswith('+'):
			return 'fail: + reserved for SMS'
		else:
			brace_handler(ID, request.form['msg'])
			return 'success'
	else:
		device = devices.find_one({'ID' : ID})
		return render_template('index.html', ID=ID, msg=device['msg'], time=device['time']) #, name=device['name'])
