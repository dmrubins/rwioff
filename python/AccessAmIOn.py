'''
Created on Nov 19, 2014

@author: David
'''

import re
import urllib.request
from bs4 import BeautifulSoup
from icalendar import Calendar
from datetime import date, timedelta, datetime
from Schedule import InternSchedule, DATESTR, Schedules
from JuniorSchedule import JuniorSchedule
from SeniorSchedule import SeniorSchedule
import pickle

########################################
BASE_URL = 'http://www.amion.com/cgi-bin/ocs'
PASSWORD = b"bwh07"
########################################

# log in to amion
req = urllib.request.Request(BASE_URL, data=b"Login=" + PASSWORD, method="POST")
f = urllib.request.urlopen(req)

#get the link to the my schedule page    
soup = BeautifulSoup(f.read())                           #soupify the page
href = soup.find(title="My schedule").parent.get('href')   #get the link to the my schedule page

#refine the my schedule link
pattern = re.compile("\./ocs(.*)") 
match = pattern.match(href)
href = match.group(1)

#opens the my schedule page
req = urllib.request.Request(BASE_URL + href) 
f = urllib.request.urlopen(req)                 

#soupify the page
soup = BeautifulSoup(f.read())
#get all the selects on the page
selects = soup.find_all("select")
#find the interns select
for select in selects:
    options = select.find('option') #find the first option
    if (options.contents[0] == "Interns\n"): #check if that option is intern
        interns = str(options.contents[1])  #stringify the options (the formatting of the website is wrong, so every option is a child of the previous option)
    if (options.contents[0] == "Juniors\n"):
        juniors = str(options.contents[1])
    if (options.contents[0] == "Seniors\n"):
        seniors = str(options.contents[1])

# Enumerate all the potential dates
start_date = datetime.now().date()
end_date = date(2015, 6, 20) #last day of this year
dates = [start_date + timedelta(i) for i in range(int ( (end_date - start_date).days ))]

def get_ica_file(vcal):
    #Download the ICA file
    req = urllib.request.Request(BASE_URL + "?Vcal=7." + vcal + "&Lo=bwh07&Jd=6558")
    f = urllib.request.urlopen(req)

    #Read the calendar into a cal variable
    return Calendar.from_ical(f.read())

#pattern to get the vcal identifier 
pattern = "<option value=\".*?14\*(.*)\*.*?>(.*)"

intern_schedules = Schedules()
junior_schedules = Schedules()
senior_schedules = Schedules()

#cycle through all the matches and grab the vcal identifier and the residents name

for m in re.finditer(pattern, interns, re.IGNORECASE):
#for i in range(1):
    vcal = m.group(1)
    intern_name = m.group(2)
    #vcal = '9045'
    #intern_name = 'Rahul'
    cal = get_ica_file(vcal)
    schedule = InternSchedule(intern_name, dates)
    schedule.create_from_ical(cal)
    intern_schedules.add(schedule)

for m in re.finditer(pattern, juniors, re.I):
    vcal = m.group(1)
    res_name = m.group(2)
    cal = get_ica_file(vcal)
    schedule = JuniorSchedule(res_name, dates)
    schedule.create_from_ical(cal)
    junior_schedules.add(schedule)

for m in re.finditer(pattern, seniors, re.I):
    vcal = m.group(1)
    res_name = m.group(2)
    cal = get_ica_file(vcal)
    schedule = SeniorSchedule(res_name, dates)
    schedule.create_from_ical(cal)
    senior_schedules.add(schedule)

#Save the file with filename lastname_firstname
with open('InternSchedules.pickle', 'wb') as f:
    pickle.dump(intern_schedules, f)

with open('JuniorSchedules.pickle', 'wb') as f:
    pickle.dump(junior_schedules, f)

with open('SeniorSchedules.pickle', 'wb') as f:
    pickle.dump(senior_schedules, f)



"""
    for d in dates:
        day = datetime.strftime(d,DATESTR)
        isOff = schedule.is_off_on(d)
        if isOff:
            temp = ((intern_name,schedule.get_block(d)),)
            if DayOff.get(day) is not None:    
                DayOff[day] = DayOff[day] + temp
            else:
                DayOff[day] = temp
    




#Open the txt file with the holiday days off
with open('holiday.txt', 'r') as f:
    for line in f:
        m = re.match('(.*?);(.*)', line)
        dt =  datetime.strptime(m.group(2).strip(), '%m/%d/%Y')
        m = re.match("(.*?), (\w*)\(?", m.group(1), re.I)
        if m:
            intern_name = m.group(2) + " " + m.group(1) 
    
        day = datetime.strftime(dt, DATESTR)
        temp = ((intern_name,"Holiday Shift"),)
        if DayOff.get(day) is not None:    
            print(intern_name)
            DayOff[day] = DayOff[day] + temp
        else:
            print(intern_name)
            DayOff[day] = temp


#Save the file with filename lastname_firstname
with open('DayOffList.pickle', 'wb') as f:
    pickle.dump(DayOff, f)
"""    