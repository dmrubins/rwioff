'''
Created on Dec 13, 2014

@author: David
'''
import pickle
from datetime import datetime, date, timedelta
from Shift import DATESTR

with open("DayOffList.pickle", 'rb') as f:
    DayOff = pickle.load(f)

# Enumerate all the potential dates
start_date = datetime.now().date()
end_date = date(2015, 6, 20) #last day of this year
dates = [start_date + timedelta(i) for i in range(int ( (end_date - start_date).days ))]

#
for d in dates:
    day = datetime.strftime(d,DATESTR)
    print('Date: {}, List: {}'.format(day, DayOff.get(day)))
    input('')