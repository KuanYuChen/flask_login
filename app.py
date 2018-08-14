"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from instagram import getfollowedby, getname

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

JSONNAME = "map.json"
def dic2json(data):
    with open(JSONNAME, 'w') as fp:
        json.dump(data, fp)

def json2dic():
    with open(JSONNAME, 'r') as fp:
        data = json.load(fp)
    return data

class User(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))

	def __init__(self, username, password):
		self.username = username
		self.password = password


@app.route('/', methods=['GET', 'POST'])
def home():
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		if request.method == 'POST':
			username = getname(request.form['username'])
			return render_template('index.html', data=getfollowedby(username))
		return render_template('index.html')

import requests
urls=[]
urls.append('http://192.168.1.149/api/hadata/0196-1')
urls.append('http://192.168.1.149/api/hadata/0196-2')
urls.append('http://192.168.1.149/api/hadata/0196-3')
urls.append('http://192.168.1.149/api/hadata/0196-5')
urls.append('http://192.168.1.149/api/hadata/0196-6')
urls.append('http://192.168.1.149/api/hadata/0196-7')
urls.append('http://192.168.1.149/api/hadata/0196-8')
urls.append('http://192.168.1.149/api/hadata/0196-9')
urls.append('http://192.168.1.149/api/hadata/0196-10')
urls.append('http://192.168.1.149/api/hadata/0196-11')
urls.append('http://192.168.1.149/api/hadata/0196-12')
urls.append('http://192.168.1.149/api/hadata/0196-13')
urls.append('http://192.168.1.149/api/hadata/0196-15')
urls.append('http://192.168.1.149/api/hadata/0196-16')
urls.append('http://192.168.1.149/api/hadata/0196-17')
urls.append('http://192.168.1.149/api/hadata/0196-18')
urls.append('http://192.168.1.149/api/hadata/0196-19')
urls.append('http://192.168.1.149/api/hadata/0196-20')
urls.append('http://192.168.1.149/api/hadata/0196-21')
urls.append('http://192.168.1.149/api/hadata/0196-22')
urls.append('http://192.168.1.149/api/hadata/0196-23')
urls.append('http://192.168.1.149/api/hadata/0196-25')
urls.append('http://192.168.1.149/api/hadata/0196-26')
urls.append('http://192.168.1.149/api/hadata/0196-27')
urls.append('http://192.168.1.149/api/hadata/0196-28')
urls.append('http://192.168.1.149/api/hadata/0196-29')
urls.append('http://192.168.1.149/api/hadata/0196-30')
urls.append('http://192.168.1.149/api/hadata/0196-31')
urls.append('http://192.168.1.149/api/hadata/0196-32')
urls.append('http://192.168.1.149/api/hadata/0196-33')


def getHdata():
	for url in urls:
		r=requests.get(url)
		tabls_data.append(r.json())
		
tabls_data=	[{
  "gtime": "20:54:29",
  "status": "offline"
},
{
  "gtime": "20:54:59",
  "status": "offline"
},
]
	
@app.route('/tabls', methods=['GET', 'POST'])
def tabls():
	#getHdata()
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		print(tabls_data)
		return render_template('tabls.html',data=tabls_data)

	
	
'''
@app.route('/', methods=['GET', 'POST'])
def home():
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		if request.method == 'POST':
			username = getname(request.form['username'])
			return render_template('index.html', data=getfollowedby(username))
		return render_template('map.html',data=devs)
'''
	

    
@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('login.html')
	else:
		name = request.form['username']
		passw = request.form['password']
		try:
			data = User.query.filter_by(username=name, password=passw).first()
			if data is not None:
				session['logged_in'] = True
				return redirect(url_for('tabls'))
			else:
				return 'Dont Login'
		except:
			return "Dont Login"

@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'POST':
		new_user = User(username=request.form['username'], password=request.form['password'])
		db.session.add(new_user)
		db.session.commit()
		return render_template('login.html')
	return render_template('register.html')


@app.route('/setmac', methods=['GET', 'POST'])
def setmac():
	"""Register Form"""
	if request.method == 'POST':
		email=request.form['email']
		mac=request.form['mac']
		#print("email"+email)
		#print("mac"+mac)
		if email in devs:
			l=devs[email]
			l.append(mac)
		else:
			l=[]
			l.append(mac)
			devs[email]=l
		return render_template('map.html',data=devs)
	return render_template('map.html',data=devs)


@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('home'))



@app.route('/map')
def map():
    global devs
    return render_template("map.html",
      data=devs,
      title='Map Table')


if __name__ == '__main__':
    global devs
    devs=json2dic()
    print(type(devs))
    print(devs)    
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0',port=9999)
	