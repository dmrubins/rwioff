from datetime import datetime
import pickle
import json


with open("JuniorSchedules.pickle", 'rb') as f:
	schedules = pickle.load(f)

with open("Residents.pickle", 'rb') as f:
	residents = pickle.load(f)


#r = residents.get_resident_by_name("Alessandra Calvo-Friedman")
#print(r)

#s = schedules.get_schedule_for_resident(r)
#s.print_schedule()


r = schedules.get_residents_off_for_date(datetime(2015,1,1))
print(r)

