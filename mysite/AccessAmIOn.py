'''
Created on Nov 19, 2014

@author: David
'''

import re
import urllib.request
from bs4 import BeautifulSoup
from icalendar import Calendar
from datetime import date, timedelta, datetime
from Shift import Schedule, DATESTR
import pickle

########################################
datestr = '%Y-%m-%d'
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


#create the list of interns that will store the vcal identifier
internstack = []

# Enumerate all the potential dates
start_date = datetime.now().date()
end_date = date(2015, 6, 20) #last day of this year
dates = [start_date + timedelta(i) for i in range(int ( (end_date - start_date).days ))]
DayOff = {}

#pattern to get the vcal identifier 
pattern = "<option value=\".*?14\*(.*)\*.*?>(.*)"
#pattern = 'skip'

#interns = '<option value="ttttt14*tttt*tttt>tttt'
#cycle through all the matches and grab the vcal identifier and the interns name
for m in re.finditer(pattern, interns, re.IGNORECASE):
    vcal = m.group(1)
    #vcal = '9029'
    intern_name = m.group(2)
    if re.search("ED Intern", intern_name, re.I) or re.search("SubI Set",  intern_name, re.I) or re.search("OB Intern", intern_name, re.I):
        continue
    
    m = re.match("(.*?), (\w*)\(?", intern_name, re.I)
    if m:
        intern_name = m.group(2) + " " + m.group(1)
    
    internstack.append(intern_name)
    
    #Download the ICA file
    req = urllib.request.Request(BASE_URL + "?Vcal=7." + vcal + "&Lo=bwh07&Jd=6558")
    f = urllib.request.urlopen(req)

    #Read the calendar into a cal variable
    cal = Calendar.from_ical(f.read())
    schedule = Schedule()
    schedule.create_from_ical(cal)
 
    print(intern_name)
 
    for d in dates:
        day = datetime.strftime(d,DATESTR)
        isOff = schedule.is_off_on(d)
        #print('Day: {}, Off: {}'.format(d, isOff))
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
    