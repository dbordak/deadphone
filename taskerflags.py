import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient(os.environ['MONGOHQ_URL'])
db = client.get_default_database()
devices = db.devices

## Example database entry
#example_phone = {
#	"name" : "phon",
#	"bat" : "1",
#	"busy" : "0",
#	"time" : "YYYY-MM-DD HH:MM:SS.SSSSSS",
#	"msg" : "hi i am not home right now please leave a message after the beep. beep."
#}
#update(example_phone)

def update(device):
	return devices.find_and_modify(
		query={"name": device["name"]},
		update=device,
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
			update({
				'name' : name,
				'msg' : request.form['msg'],
				'time' : datetime.strftime(datetime.now(),"%a %b %d, %Y - %I:%M %p")
			})
			return 'success'
	else:
		device = devices.find_one({'name' : name})
		return render_template('index.html', name=name, msg=device['msg'], time=device['time'])
