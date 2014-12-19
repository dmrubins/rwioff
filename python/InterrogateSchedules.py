from Schedule import Schedules
import pickle
from datetime import datetime

with open('InternSchedules.pickle', 'rb') as f:
    intern_schedules = pickle.load(f)

t = intern_schedules.get_residents_off_for_date( datetime.now() )
j = { "names" : [x[0] for x in t],
         "blocks" : [x[1] for x in t]}
print(j)