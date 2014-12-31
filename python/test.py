from datetime import datetime
import pickle
import json


with open("JuniorSchedules.pickle", 'rb') as f:
	schedules = pickle.load(f)

with open("Residents.pickle", 'rb') as f:
	residents = pickle.load(f)


def intersect_residents(ids):
	global schedules

	#Parse the ids
	ids = ids.split(";")
	return {"id" : [x[0] for x in ids]}

print(intersect_residents('12345678'))