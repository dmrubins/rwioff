
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from datetime import datetime
import pickle
import json
import os
import re

if os.name is 'nt':
	base =  "c:/users/david/copy/dev/rwioff/"
else:
	base = "/home/dmrubins/site/"

with open(base + "python/Schedules.pickle", 'rb') as f:
    schedules = pickle.load(f)
with open(base + "python/Residents.pickle", 'rb') as f:
	residents = pickle.load(f)

app = Flask(__name__, static_folder=base + "static/")

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

def json_residents_off(dt, pgy):
	global schedules
	t = schedules.get_residents_off_for_date( dt, pgy )
	j = { "names" : [x[0] for x in t], "blocks" : [x[1] for x in t] }
	return json.dumps(j)

@app.route("/interns/off/<date>")
def get_interns_for_date(date):
	dt = datetime.strptime(date, '%Y%m%d')
	return json_residents_off(dt, 1)

@app.route("/juniors/off/<date>")
def get_juniors_for_date(date):
	dt = datetime.strptime(date, '%Y%m%d')
	return json_residents_off(dt, 2)

@app.route("/seniors/off/<date>")
def get_seniors_for_date(date):
	dt = datetime.strptime(date, '%Y%m%d')
	return json_residents_off(dt, 3)

@app.route("/residents/")
def get_residents():
	global residents
	r = residents.get_residents()
	return json.dumps({"names" : [x.get_name() for x in r], "ids" : [x.get_id() for x in r]})

@app.route('/intersect/<ids>')
def intersect_residents(ids):
	global schedules
	ids = re.findall('\d{4}', ids)
	dates = schedules.intersect_schedules(ids)
	return json.dumps( {'dates' : [ datetime.strftime(x, "%Y%m%d") for x in dates ]} )

print(intersect_residents('44799005'))