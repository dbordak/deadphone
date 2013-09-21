import os
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(os.environ['MONGOHQ_URL'])
db = client.get_default_database()
devices = db.devices
example_phone = {
	"name" : "phon",
	"battery" : "1",
	"busy" : "0",
	"timestamp" : "i do not know what the format of this is supposed to beeeeeee",
	"message" : "hi i am not home right now please leave a message after the beep. beep."
}
#UID = devices.insert(example_phone) #Insertion returns a unique ID; this may not be needed. Only time will tell.
update(example_phone);

def update(device):
	return devices.findAndModify( {
		query : {"name" : device.name},
		update : device,
		upsert : true
	})

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<username>', methods=['GET', 'POST'])
def profile(username):
	if request.method == 'POST':
		return 'TODO: add message to database'
	else:
		return render_template('index.html', username=username) #TODO fetch messages
