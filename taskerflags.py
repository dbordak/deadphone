import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient(os.environ['MONGOHQ_URL'])
db = client.get_default_database()
devices = db.devices
example_phone = {
	"name_goes_here" : "status message"
}
UID = devices.insert(example_phone) #Insertion returns a unique ID; this may not be needed. Only time will tell.
#TODO do things with this

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<username>', methods=['GET', 'POST'])
def profile(username):
	if request.method == 'POST':
		devices.insert({
			'username' : request.form['username'],
			'message' : request.form['message'],
			'time' : str(datetime.now())
			})
		return 'TODO: add message to database'
	else:
		return render_template('index.html', username=username) #TODO fetch messages
