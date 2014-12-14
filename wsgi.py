#!/usr/bin/env python

from flask import Flask
from _datetime import datetime
from Shift import DATESTR
import pickle
import json

global DayOff
app = Flask(__name__)

@app.route("/residents/<date>")
def get_residents_for_date(date):
    global DayOff
    dt = datetime.strptime(date, '%Y%m%d')
    t = DayOff.get(datetime.strftime(dt, DATESTR))
    j = { "names" : [x[0] for x in t],
         "blocks" : [x[1] for x in t]}
    return json.dumps(j)

if __name__ == "__main__":
    with open("DayOffList.pickle", 'rb') as f:
        DayOff = pickle.load(f)
    app.run()