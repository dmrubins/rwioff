'''
Created on Dec 7, 2014

@author: David
'''
from datetime import datetime
import re
from _datetime import timedelta, time, date
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

    def get(self, dt):
        return self.shifts.get(datetime.strftime(dt, DATESTR))

class Blocks():
    def __init__(self):
        self.blocks = {}

    def add(self, block):
        day = block.get_day()
        self.blocks[day] = block

    def get(self, dt):
        return self.blocks.get( datetime.strftime(dt,DATESTR) )

class Schedule():
    
    def __init__(self, date_range):
        self.blocks = Blocks()
        self.shifts = Shifts()
        self.date_range = date_range
    
    def _add_ica_event_to_schedule(self, start_date, end_date, summary):
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
    
    def _fix_up_calendar(self):
        return

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
                    self._add_ica_event_to_schedule(starts[i], ends[i], summary)
                    
            else:
                self._add_ica_event_to_schedule(start_date, end_date, summary)

        self._fix_up_calendar();
    
    def add_block(self, block):
        #print('Date: {}, Block: {}'.format(block.get_day(), block.get_summary()))
        self.blocks.add(block)
        
    def add_shift(self, shift):
        self.shifts.add(shift)
            
    def get_shift_for_date(self, dt):
        return self.shifts.get(dt)
    
    def is_off_on(self, dt):
        shift = self.shifts.get(dt) # get the shift for the date
        if shift is not None:
            #print('On {}, you are on {}'.format(date, shift.get_summary()))
            return False
            
        if shift is None: #if there is no shift for that day    
        #    print('On {}, you are on None'.format(date))

            block = self.blocks.get(datetime.strftime(dt, DATESTR)) # get the block for the day
            if block is None:
                return True
            
            isWeekend = dt.weekday() == 5 or dt.weekday() == 6
            isHoliday = dt > date(2014,12,23) and dt < date(2015,1,3)
            isVacation = self.is_block_(block, "vac") or self.is_block_(block, "hol")
            
            #print('Date: {}, isHoliday: {}'.format(datetime.strftime(dt, DATESTR), isHoliday))
            
            #Is it a holiday/vacation
            if isHoliday and isVacation:
                return True
            elif isHoliday:
                return False                
            
            #If off medicine service
            if self.is_block_(block, "OFF"):
                return False
            
            # Check if Amby week
            isAmby = self.is_block_(block, "Amb") or self.is_block_(block, "pcar") or self.is_block_(block, "hvm")
            isElec = self.is_block_(block, "elec")
            isPeds = self.is_block_(block, "PEDS")
            isAnesth = self.is_block_(block, "Anesth") or self.is_block_(block, "Blood")
            if isAmby or isElec or isPeds or isAnesth:
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
                    previous_date = dt - timedelta(1) #Get previous day
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
    
    def get_block(self, dt):
        block = self.blocks.get( datetime.strftime(dt, DATESTR) )
        if block is None:
            return "Unknown"
        return block.get_summary()

class InternSchedule(Schedule):

    def _get_block_name_from_shift(self, shift):
        
        # Format of XXXX long/short intern #
        # ITU, MICU, GMS, VA-Cards, CHF, Onc-A, Onc-C, CCU, MICU, Cards, FGMS
        #print( shift.get_summary() )
        m = re.search('(?:Call )?(.*?) (?:long|short|post-night) ', shift.get_summary(), re.I)
        if m is not None:
            return m.group(1)


        m = re.search('(.*?)intern (.*?) ', shift.get_summary(), re.I)
        if m is not None:
            block = m.group(1) + m.group(2)
            return block
            print( "block: {}".format(block) )
        # Format of XXX intern XXX
        # Onc nightfloat

        # XXXX twilight intern 
        # GMS
        



        return

    def _get_shift_from_block(self, block, next_shift):
        #todo
        return

    def _fix_up_calendar(self):
        for dt in self.date_range:

            # Get the block/shift for the day
            block = self.blocks.get(dt)
            shift = self.shifts.get(dt)
            
            # If both the block and shift don't exist, look at the previous/next day
            if block is None and shift is None:
                next_shift = self.shifts.get( dt + timedelta(1) )
                if next_shift is None:
                    #TODO
                    continue
                block_name = self._get_block_name_from_shift(next_shift)

            # If the block doesn't exist, look at the shift
            elif block is None:
                block_name = self._get_block_name_from_shift(shift)

            # If the shift doesn't exist, look at the block
            if shift is None:
                next_shift = self.shifts.get( dt + timedelta(1) )
                shift = self._get_shift_from_block(block, next_shift)

            # Add the block/shift back to the maps
            if shift is not None and block is not None:
                self.blocks.add( Block(dt, block_name) )
                self.shifts.add(shift)












