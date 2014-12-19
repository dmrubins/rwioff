from Schedule import Schedules
import pickle
from datetime import datetime

with open('DayOffList.pickle', 'rb') as f:
    intern_schedules = pickle.load(f)

print(intern_schedules.get_residents_off_for_date( datetime.now() ))