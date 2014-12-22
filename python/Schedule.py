'''
Created on Dec 7, 2014

@author: David
'''
import re
from datetime import timedelta, time, date, datetime
from dateutil.rrule import *

DATESTR = '%Y-%m-%d'

class Shift():
    
    def __init__(self, start_dt=datetime.now(), end_dt = datetime.now(), summary = None):
        self.summary = summary
        self.start_dt = start_dt
        self.end_dt = end_dt

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

    def is_day_off(self):
        return False

class DayOff(Shift):
    def __init__(self, dt):
        Shift.__init__(self, dt, dt, "Day Off")
   
    def is_day_off(self):
        return True

class Block():
    
    def __init__(self, dt, summary):
        if not hasattr(dt, "time"):
            dt = datetime.combine(dt, datetime.now().replace(hour=0).time())
        self.dt = dt
        self.summary = summary

    def get_day(self):
        return datetime.strftime(self.dt, DATESTR)

    def get_summary(self):
        return self.summary

    def is_(self, block_name):
        #print(self.get_summary())
        return re.search(block_name, self.get_summary(), re.IGNORECASE)

class Shifts():
    
    def __init__(self):
        self.shifts = {}
        
    def add(self, shift):
        if re.search("Jen Ctr", shift.get_summary(), re.I):
            return
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
    
    def __init__(self, resident, date_range):
        self.blocks = Blocks()
        self.shifts = Shifts()
        self.date_range = date_range
        self.resident = resident
        self.tzinfo = None
        print(self.resident.get_name())

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
        for dt in self.date_range:

            # Get the block/shift for the day
            block = self.blocks.get(dt)
            shift = self.shifts.get(dt)
            
            if block is None:
                #print(dt)
                #if shift is not None:
                #    print("Shift is {} ".format(shift.get_summary()))
                # If both the block and shift don't exist, look at the previous/next day
                if shift is None or re.search("(AM:|PM:)", shift.get_summary(), re.I):
                    next_shift = self.shifts.get( dt + timedelta(1) )
                    prev_shift = self.shifts.get( dt - timedelta(1) )
                    if next_shift is None:
                        if prev_shift is None:
                            block_name = "Vacation"
                        else:
                #            print("Previous shift {}".format(prev_shift.get_summary()))
                            block_name = self._get_block_name_from_shift(prev_shift)
                #            print('Look at previous shift: {}'.format(block_name))
                    else:
                #        print('Next shift is {}:'.format(next_shift.get_summary()))
                        block_name = self._get_block_name_from_shift(next_shift)
                #        print('Look at next shift: {}'.format(block_name))
               
                # If the block doesn't exist, look at the shift
                else:
                    block_name = self._get_block_name_from_shift(shift)
                #    print('Look at current shift: {}'.format(block_name))

                if re.search("none", block_name, re.I):
                    input('')

                #Create the new block using derived data
                block = Block(dt, block_name)
                self.blocks.add( block )

        #Separate out the shift from the block to do the prev/next look correctly
        for dt in self.date_range:
            # Get the block/shift for the day
            block = self.blocks.get(dt)
            shift = self.shifts.get(dt)

            # If is holiday, then set standard shift continue
            if dt > date(2014,12,23) and dt < date(2015,1,3) and not (block.is_('Holiday') or block.is_('Vacation') or block.is_('hol-vac') ):
                sss = datetime.combine(dt, datetime.now().replace(hour=7).time())
                sse = datetime.combine(dt, datetime.now().replace(hour=5).time())
                standard_shift = Shift(sss, sse, block.get_summary())
                self.shifts.add( standard_shift )
                continue
            

            # If the shift doesn't exist, look at the block
            if shift is None:
                prev_shift = self.shifts.get( dt - timedelta(1) )
                shift = self._get_shift_from_block(block, prev_shift)
                self.shifts.add( shift )                

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
        if self.tzinfo is None:
            self.tzinfo = shift.start_dt.tzinfo
        self.shifts.add(shift)
            
    def get_shift_for_date(self, dt):
        return self.shifts.get(dt)
    
    def get_resident(self):
        return self.resident

    def is_off_on(self, dt):
        shift = self.shifts.get(dt)
        return shift.is_day_off()
    
    def get_all_days_off(self):
        days = set() 
        for dt in self.date_range:
            if self.is_off_on(dt):
                days.add( dt )
        return days

    def get_block(self, dt):
        block = self.blocks.get( dt )
        if block is None:
            return "Unknown"
        return block.get_summary()

class Schedules():

    def __init__(self):
        self.schedules = {}

    def add(self, schedule):
        resident_id = schedule.get_resident().get_id()
        self.schedules[resident_id] = schedule

    def get_residents_off_for_date(self, dt):
        off_residents = []
        for i in self.schedules:            
            s = self.schedules[i]
            if s.is_off_on(dt):
                off_residents.append( (s.get_resident().get_name(), s.get_block(dt)) )
        return off_residents

    def get_schedule_for_resident(self, resident):
        return self.schedules.get(resident.get_id())
        
    def intersect_schedules(self, *args):
        days_off = set(self.schedules[1].date_range)
        for i in range(len(args)):
            s = self.get_schedule_for_resident(r[i])
            days_off = days_off & s.get_all_days_off()

        return days_off
        #Intersect days off