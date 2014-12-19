
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from datetime import datetime
import pickle
import json
from Schedule import DATESTR

global intern_schedules
with open("/home/dmrubins/site/python/InternSchedules.pickle", 'rb') as f:
    intern_schedules = pickle.load(f)
with open("/home/dmrubins/site/python/JuniorSchedules.pickle", 'rb') as f:
    junior_schedules = pickle.load(f)
with open("/home/dmrubins/site/python/SeniorSchedules.pickle", 'rb') as f:
    senior_schedules = pickle.load(f)


app = Flask(__name__)

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

def json_residents_off(dt, schedules):
	t = schedules.get_residents_off_for_date( dt )
    j = { "names" : [x[0] for x in t], "blocks" : [x[1] for x in t]}
    return json.dumps(j)

@app.route("/interns/off/<date>")
def get_interns_for_date(date):
    global intern_schedules
    dt = datetime.strptime(date, '%Y%m%d')
	return json_residents_off(dt, intern_schedules)    

@app.route("/juniors/off/<date>")
def get_interns_for_date(date):
    global junior_schedules
    dt = datetime.strptime(date, '%Y%m%d')
	return json_residents_off(dt, junior_schedules)    

@app.route("/seniors/off/<date>")
def get_interns_for_date(date):
    global senior_schedules
    dt = datetime.strptime(date, '%Y%m%d')
	return json_residents_off(dt, senior_schedules)    
