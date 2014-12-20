from Schedule import Schedules, Schedule, DayOff
import pickle
from datetime import datetime
import re

with open("InternSchedules.pickle", 'rb') as f:
    intern_schedules = pickle.load(f)
with open("JuniorSchedules.pickle", 'rb') as f:
    junior_schedules = pickle.load(f)
with open("SeniorSchedules.pickle", 'rb') as f:
    senior_schedules = pickle.load(f)

#Open the txt file with the holiday days off
with open('Holiday Schedule.txt', 'r') as f:
    for line in f:
        m = re.match('\"(.*?)\".*;(.*)', line)
        if m is not None:
            dt =  datetime.strptime(m.group(2).strip(), '%m/%d/%Y')
            name = Schedule.fix_name(m.group(1))
        else:
            name = "Shubhangi"
    
        s = intern_schedules.get_schedule_for_resident(name)
        if s is None:
            s = junior_schedules.get_schedule_for_resident(name)
            if s is None:
                s = senior_schedules.get_schedule_for_resident(name)

        if s is None:
            print("Error finding schedule for {}".format(name))
            input('')

        s.add_shift( DayOff(dt) )
        print( s.is_off_on(dt) )