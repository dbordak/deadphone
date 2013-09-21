import os
from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(os.environ['MONGOHQ_URL'])
mongo_db = client.get_default_database()
#TODO do things with this

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/u/<username>', methods=['GET', 'POST'])
def profile(username):
	if request.method == 'POST':
		return 'TODO: add message to database'
	else:
		return username #TODO fetch messages
