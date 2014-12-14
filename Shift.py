'''
Created on Dec 7, 2014

@author: David
'''
from datetime import datetime
import re
from _datetime import timedelta, time
from dateutil.rrule import *

DATESTR = '%Y-%m-%d'

class Shift():
    
    def set_summary(self, summary):
        self.summary = summary

    def set_start(self, start_dt):
        self.start_dt = start_dt.astimezone()
        
    def set_end(self, end_dt):
        self.end_dt = end_dt.astimezone()
        if self.start_dt + timedelta(1) == self.end_dt:
            self.end_dt = self.end_dt - timedelta(hours=1)

    def get_day(self):
        if self.end_dt.date() != self.start_dt.date() and self.end_dt.time().hour > 10:
            return (datetime.strftime(self.start_dt, DATESTR), datetime.strftime(self.end_dt, DATESTR))
        else:
            return (datetime.strftime(self.start_dt, DATESTR), )

    def get_summary(self):
        return self.summary

class Block():
    
    def __init__(self, dt, summary):
        self.dt = dt
        self.summary = summary

    def get_day(self):
        return datetime.strftime(self.dt, DATESTR)
    
    def get_summary(self):
        return self.summary


class Shifts():
    
    def __init__(self):
        self.shifts = {}
        
    def add(self, shift):
        day = shift.get_day()
        for d in day:
            self.shifts[d] = shift

    def get(self, date):
        return self.shifts.get(datetime.strftime(date, DATESTR))

class Schedule():
    
    def __init__(self):
        self.blocks = {}
        self.shifts = Shifts()
    
    def _addToSchedule(self, start_date, end_date, summary):
        #print("Start: {}, End: {}, Summary: {}".format(start_date, end_date, summary))
        isBlock = start_date == end_date
    
        if not isBlock:
            shift = Shift()
            shift.set_summary( summary )
            shift.set_start( start_date )
            shift.set_end( end_date )
            self.add_shift( shift )
        else:
            self.add_block( Block(start_date, str(summary)) )
    
    def create_from_ical(self, cal):
        for component in cal.walk('vevent'):
    
            start_date = component.get('dtstart').dt
            end_date = component.get('dtend').dt
            summary = component.get('summary')
    
            recur = component.get('RRULE')
            if recur is not None:
                FREQ, COUNT, INTERVAL = "", "", ""
                #Get the frequency    
                m = re.search("'FREQ': \['(.*?)'\]", str(recur), re.IGNORECASE)
                FREQ = m.group(1)
                #Get the Count
                m = re.search("'COUNT': \[(.*?)\]", str(recur), re.IGNORECASE)
                COUNT = int(m.group(1))
                #Get the interval
                m = re.search("'INTERVAL': \[(.*?)\]", str(recur), re.IGNORECASE)
                INTERVAL = int(m.group(1))
        
                #Expand out the dates
                starts = list(rrule(DAILY, count=COUNT, interval=INTERVAL, dtstart=start_date))
                ends = list(rrule(DAILY, count=COUNT, interval=INTERVAL, dtstart=end_date))
        
                for i in range(len(starts)):
                    self._addToSchedule(starts[i], ends[i], summary)
                    
            else:
                self._addToSchedule(start_date, end_date, summary)
    
    def add_block(self, block):
        #print('Date: {}, Block: {}'.format(block.get_day(), block.get_summary()))
        self.blocks[block.get_day()] = block
        
    def add_shift(self, shift):
        self.shifts.add(shift)
            
    def get_shift_for_date(self, date):
        return self.shifts.get(date)
    
    def is_off_on(self, date):
        shift = self.shifts.get(date) # get the shift for the date
        if shift is not None:
            #print('On {}, you are on {}'.format(date, shift.get_summary()))
            return False
            
        if shift is None: #if there is no shift for that day    
        #    print('On {}, you are on None'.format(date))

            isWeekend = date.weekday() == 5 or date.weekday() == 6
            block = self.blocks.get(datetime.strftime(date, DATESTR)) # get the block for the day
            
            if block is None:
                return True
            
            # Check if Amby week
            isAmby = self.is_block_(block, "Amb")
            isPCARE = self.is_block_(block, "pcar")
            if isAmby or isPCARE:
                if isWeekend:  # on Amby, you get weekends off
                    return True
                else:
                    return False
        
            # Check if Cards
            isCards = self.is_block_(block, "cards")
            isFGMS = self.is_block_(block, "FGMS")
            isVAGMS = self.is_block_(block, "VA-GMS")
            if isFGMS or isCards or isVAGMS:
                if isWeekend:
                    #If on call Friday, you're on on Saturday
                    previous_date = date - timedelta(1) #Get previous day
                    previous_shift = self.shifts.get(previous_date) # Get previous shift
                    if previous_date.weekday() == 4 and previous_shift is not None: #If previous day is Friday and their was a shift
                        if re.search("long", previous_shift.get_summary(), re.IGNORECASE):
                            return False
                        else:
                            return True
                    else:
                        return True                    
                else:
                    return False
        
            # Check if BMT or CHF
            isBMT = self.is_block_(block, "BMT")
            isCHF = self.is_block_(block, "CHF")
            if isBMT or isCHF:
                if isWeekend:
                    return True
                else:
                    return False
        
        return True
    
    def is_block_(self, block, block_title):
        return re.search(block_title, block.get_summary(), re.IGNORECASE)
    
    def get_block(self, date):
        block = self.blocks.get( datetime.strftime(date, DATESTR) )
        if block is None:
            return "Unknown"
        return block.get_summary()