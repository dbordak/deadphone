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
#	"time" : "i do not know what the format of this is supposed to beeeeeee",
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

@app.route('/<username>', methods=['GET', 'POST'])
def profile(username):
	if request.method == 'POST':
		update({
			'name' : username,
			'msg' : request.form['msg'],
			'time' : str(datetime.now())
			})
		return 'success'
	else:
		device = devices.find_one({'name' : name})
		return render_template('index.html', username=username, msg=device['msg'], time=device['time']) #TODO fetch messages
