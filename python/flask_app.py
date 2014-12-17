
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from _datetime import datetime
import pickle
import json
from Schedule import DATESTR

global DayOff
with open("/home/dmrubins/site/python/DayOffList.pickle", 'rb') as f:
    DayOff = pickle.load(f)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.route("/residents/<date>")
def get_residents_for_date(date):
    global DayOff
    dt = datetime.strptime(date, '%Y%m%d')
    t = DayOff.get(datetime.strftime(dt, DATESTR))
    j = { "names" : [x[0] for x in t],
         "blocks" : [x[1] for x in t]}
    return json.dumps(j)