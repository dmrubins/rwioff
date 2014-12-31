import re

class Resident():
    @classmethod
    def fix_name(cls, n):
        m = re.search("(.*?), (\w*)\(?", n, re.I)
        if m is not None:
            lastname = m.group(1)
            firstname = m.group(2)
        else:
            return "Shubhangi"

        m = re.search("\((.*?)\)", n, re.I)
        if m is not None and re.search("(MD|MM|Neu|Pre|Neu|HVMA|DGM|GHE|MP|MA|HEMI|MBA)", m.group(1)) is None:
            firstname = m.group(1)

        return firstname + " " + lastname

    def __init__(self, vcal, name, pgy):
        self.id = vcal
        self.name = Resident.fix_name(name)
        self.pgy = pgy

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def is_pgy(self, pgy):
        return pgy == self.pgy

class Residents():

    def __init__(self, residents):
        self.residents = residents

    def add(self, resident):
        self.residents.add(resident)

    def get_resident_by_name(self, name):
        if re.search(",", name, re.I):
            name = Resident.fix_name(name)

        for r in self.residents:
            if re.search(name, r.get_name(), re.I):
                print("Match: {}".format(name))
                return r

        print("Not found: {}".format(name))

    def get_residents(self):
        return self.residents