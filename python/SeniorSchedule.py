from Schedule import Schedule, Shift, DayOff
import re

class SeniorSchedule(Schedule):

    def _get_block_name_from_shift(self, shift):
        
        # Format of XXXX long/short intern #
        # ITU, MICU, GMS, VA-Cards, CHF, Onc-A, Onc-C, CCU, MICU, Cards, FGMS
        #print( shift.get_summary() )
        m = re.search('(?:Call )?(.*?) (?:long|short|post-night) ', shift.get_summary(), re.I)
        if m is not None:
            return m.group(1)

        # VA-Cards resident
        m = re.search('(.*?) resident', shift.get_summary(), re.I)
        if m is not None:
            return m.group(1)

        # XXXX twilight intern 
        # GMS
        m = re.search('(.*?) twilight', shift.get_summary(), re.I )        
        if m is not None:
            return m.group(1) + 'Twilight'

        # Cards nightfloat resident
        m = re.search('(.*?) nightfloat', shift.get_summary(), re.I)
        if m is not None:
            return m.group(1) + "Nightfloat"

        m = re.search('(.*?) flex', shift.get_summary(), re.I)
        if m is not None:
            return m.group(1) + "Nightfloat"

        m = re.search('DPH', shift.get_summary(), re.I)
        if m is not None:
            return "DPH"

        m = re.search("HUHS", shift.get_summary(), re.I)
        if m is not None:
            return "Amb"

        m = re.search("(.*?) NF", shift.get_summary(), re.I)
        if m is not None:
            return m.group(1) + "Nightfloat"



    def _get_shift_from_block(self, block, prev_shift):
        
        dt = block.dt
        isWeekend = dt.weekday() == 5 or dt.weekday() == 6            
        standard_shift = Shift(dt.replace(hour=7), dt.replace(hour=17), block.get_summary())
        flex_shift = Shift(dt.replace(hour=17), dt.replace(hour=23), block.get_summary())
        day_off = DayOff(block.dt)

        # For Amby, elective, peds, anesthesia, assume that all weekday shifts are 8-5
        if block.is_("Amb") or block.is_("pcar") or block.is_("hvm") \
        or block.is_("elec") or block.is_("PEDS") or block.is_("Blood") \
        or block.is_("Anesth") or block.is_('geria') or block.is_("GHE") \
        or block.is_('Jen Ctr') or block.is_('MLT') or block.is_("derm") \
        or block.is_('hbs'):
            if isWeekend:
                return day_off
            else:
                shift = Shift()
                shift.set_summary("Amby")
                shift.set_start(dt.replace(hour=8, tzinfo=self.tzinfo))
                shift.set_end(dt.replace(hour=17, tzinfo=self.tzinfo))
                return shift

        # CCU, ITU, Onc nightfloat, MICU
        if block.is_("ITU") or block.is_("CCU") or block.is_("Onc nightfloat") or block.is_("MICU") or block.is_("Onc-") or block.is_("FICU") or block.is_("Onc flt") \
        or block.is_('phys') or block.is_("vacation") or block.is_("Holiday") or block.is_("ED") or block.is_("Day off giver") or block.is_("hol-vac") or block.is_("DPH"):
            return day_off

        # For GMS, BMT and CHF, if you don't have a shift on the weekend, you're off
        # If you don't have a shift on a weekday, you're the short intern
        if block.is_("GMS") or block.is_("BMT") or block.is_("CHF") or block.is_("OFF") or block.is_('hem') or block.is_("teach") or block.is_('CMR'):
            if isWeekend:
                return day_off
            else:
                return standard_shift

        # B team, VA-GMS, FGMS, VA-Cards
        # If you don't have a shift on a weekend, and the previous day you were long, then you are on
        # If you don't have a shift on a weekday, then you are pre/post call
        if block.is_("cards") or block.is_("VA-GMS") or block.is_("FGMS") or block.is_("VA-Cards"):
            if isWeekend:
                if prev_shift is None or not re.search("long", prev_shift.get_summary(), re.I):
                    return day_off
            return standard_shift
        
        # VA-FLT
        if block.is_("VA-FLT") or block.is_("VA FLT"):
            return day_off

        if block.is_("ONC flex"):
            return standard_shift

        print("Get shift failed; Block: {}, Date: {}".format(block.get_summary(), block.dt))
        input("")
