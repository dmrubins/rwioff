from datetime import datetime
import pickle
import json


with open("InternSchedules.pickle", 'rb') as f:
    intern_schedules = pickle.load(f)

def json_residents_off(dt, schedules):
	t = schedules.get_residents_off_for_date( dt )
	j = { "names" : [x[0] for x in t], "blocks" : [x[1] for x in t] }
	return json.dumps(j)

def get_interns_for_date(date):
	global intern_schedules
	dt = datetime.strptime(date, '%Y%m%d')
	return json_residents_off(dt, intern_schedules)

print( get_interns_for_date('20141222') )