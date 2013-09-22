import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime
import twilio.twiml

app = Flask(__name__)

client = MongoClient(os.environ['MONGOHQ_URL'])
db = client.get_default_database()
devices = db.devices

plu_start_g = " they're"
plu_start_b = " they have"
sing_start_g = " is"
sing_start_b = " is"

batstring_good = " charged up and good to go."
batstring_bad  = " found themselves plagued by their current lack of current."

string_busy      = " is currently busy"
string_available = " is able to talk, as far as we know"

plu_end = ", "
sing_end = "."

conjunction_p = "and"
conjunction_n = "but"

## Device object
# ID   - used for url, when accessed via SMS this is the phone number
# msg  - short informational message
# time - timestamp of last update
# bat  - current battery status. -1 for critical, 1 for feelin' fine.
# avail - current google calendar availability status. -1 for avail, 1 for available.

def update_device(ID, msg, **kwargs):
	if devices.find_one({'ID' : ID}):
		device = devices.find_one({'ID' : ID})
	else:
		device = {'ID' : ID}
	device['time'] = datetime.strftime(datetime.now(),'%a %b %d, %Y - %I:%M %p')
	if len(kwargs):
		if kwargs.keys()[0] == 'bat':
			device['bat']=kwargs['bat']
		if kwargs.keys()[0] == 'avail':
			device['avail']=kwargs['avail']
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
		if opt[0] == "avail":
			update_device(ID, body, avail=opt[1])
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
		keys = device.keys()
		if "name" in keys:
			name = device['name']
		else:
			name = ID
		if "bat" in keys:
			bat = int(device['bat'])
			if bat == 1:
				bstring = batstring_good
			elif bat == -1:
				bstring = batstring_bad
			else:
				bstring = ""
		else:
			bstring = ""
			cstring = ""
		if "avail" in keys:
			avail = int(device['avail'])
			if avail == 1:
				astring = string_available
			elif avail == -1:
				astring = string_busy
			else:
				astring = ""
			if bat:
				conj = int(avail)*int(bat)
				if conj == 1:
					cstring = conjunction_p
				if conj == -1:
					cstring = conjunction_n
		else:
			astring = ""
			cstring = ""
		if len(cstring):
			status = name + astring + cstring + bstring
		else:
			status = ""
		return render_template('index.html', name=name, msg=device['msg'], time=device['time'], status=status)
