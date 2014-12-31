'''
Created on Nov 19, 2014

@author: David
'''

import re
import urllib.request
from bs4 import BeautifulSoup
from icalendar import Calendar
from datetime import date, timedelta, datetime
from Schedule import Schedules
from InternSchedule import InternSchedule
from JuniorSchedule import JuniorSchedule
from SeniorSchedule import SeniorSchedule
from Resident import Resident, Residents
import pickle

########################################
BASE_URL = 'http://www.amion.com/cgi-bin/ocs'
PASSWORD = b"bwh07"
########################################


########################################
def get_ica_file(vcal):
    #Download the ICA file
    req = urllib.request.Request(BASE_URL + "?Vcal=7." + vcal + "&Lo=bwh07&Jd=6558")
    f = urllib.request.urlopen(req)

    #Read the calendar into a cal variable
    return Calendar.from_ical(f.read())


def create_schedules_from_ica(resident_str, scheduleClass, pgy):
    #pattern to get the vcal identifier 
    pattern = "<option value=\".*?14\*(.*)\*.*?>(.*)"
    
    # Enumerate the date range
    start_date = datetime.now().date()
    end_date = date(2015, 6, 20) #last day of this year
    dates = [start_date + timedelta(i) for i in range(int ( (end_date - start_date).days ))]

    s = Schedules()
    r = set()
    for m in re.finditer(pattern, resident_str, re.IGNORECASE):
        vcal = m.group(1)
        res_name = m.group(2)
        if re.search("(SubI|OB I|ED Intern)", res_name, re.I):
            #print(res_name)
            continue 
        resident = Resident(vcal, res_name, pgy)
        cal = get_ica_file(vcal)
        schedule = scheduleClass(resident, dates)
        schedule.create_from_ical(cal)
        s.add(schedule)
        r.add(resident)
    return s, r

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

#cycle through all the matches and grab the vcal identifier and the residents name
intern_schedules, interns = create_schedules_from_ica(interns, InternSchedule, 1)
junior_schedules, juniors = create_schedules_from_ica(juniors, JuniorSchedule, 2)
senior_schedules, seniors = create_schedules_from_ica(seniors, SeniorSchedule, 3)

residents = Residents(interns | juniors | seniors)
schedules = Schedules(intern_schedules, junior_schedules, senior_schedules)

# Compile a list of residents
with open('Residents.pickle', 'wb') as f:
    pickle.dump(residents, f)

#Save the file with filename lastname_firstname
with open('Schedules.pickle', 'wb') as f:
    pickle.dump(schedules, f)