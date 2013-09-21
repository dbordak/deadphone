import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<username>', methods=['GET', 'POST'])
def profile(username):
	if request.method == 'POST':
		return 'TODO: add message to database'
	else:
		return username #TODO fetch messages
