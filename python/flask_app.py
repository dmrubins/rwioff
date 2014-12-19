
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from _datetime import datetime
import pickle
import json
from Schedule import DATESTR

global intern_schedules
with open("/home/dmrubins/site/python/InternSchedules.pickle", 'rb') as f:
    intern_schedules = pickle.load(f)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.route("/interns/off/<date>")
def get_interns_for_date(date):
    global intern_schedules
    dt = datetime.strptime(date, '%Y%m%d')
    t = intern_schedules.get_residents_off_for_date( dt )
    j = { "names" : [x[0] for x in t],
         "blocks" : [x[1] for x in t]}
    return json.dumps(j)

