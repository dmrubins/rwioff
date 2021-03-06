from Schedule import Schedules, Schedule, DayOff
from Resident import Resident
import pickle
from datetime import datetime
import re

with open("InternSchedules.pickle", 'rb') as f:
    intern_schedules = pickle.load(f)
with open("JuniorSchedules.pickle", 'rb') as f:
    junior_schedules = pickle.load(f)
with open("SeniorSchedules.pickle", 'rb') as f:
    senior_schedules = pickle.load(f)
with open("Residents.pickle", 'rb') as f:
	residents = pickle.load(f)

#Open the txt file with the holiday days off
with open('Holiday Schedule.txt', 'r') as f:
    for line in f:
        m = re.match('\"(.*?)\".*;(.*)', line)
        if m is not None:
            dt =  datetime.strptime(m.group(2).strip(), '%m/%d/%Y')
            name = m.group(1)
    
        resident = residents.get_resident_by_name( name )

        s = intern_schedules.get_schedule_for_resident(resident)
        if s is None:
            s = junior_schedules.get_schedule_for_resident(resident)
            if s is None:
                s = senior_schedules.get_schedule_for_resident(resident)

        if s is None:
            print("Error finding schedule for {}".format(name))

        s.add_shift( DayOff(dt) )

#Save the file with filename lastname_firstname
with open('InternSchedules.pickle', 'wb') as f:
    pickle.dump(intern_schedules, f)

with open('JuniorSchedules.pickle', 'wb') as f:
    pickle.dump(junior_schedules, f)

with open('SeniorSchedules.pickle', 'wb') as f:
    pickle.dump(senior_schedules, f)