from Patient import *
from Personnel import *
import uuid


# quarantine is very similar to hospital therefore so are the functions
class quarantine:
    def __init__(self, name, capacity):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.capacity = int(capacity)
        self.patients = []
        self.staff = []

    def occupancy(self):
        if self.capacity != 0:
            return 100 * len(self.patients) / self.capacity
        return 0

    def admission(self, name, dob):
        p = Patient(name, dob)
        self.patients.append(p)

    def serialize(self):
        return {
            'id': self.ID,
            'name': self.name,
            'capacity': self.capacity,
            'occupancy': self.occupancy(),
        }

    def addPersonnel(self, name, dob, type_):
        s = Staff(name, dob, type_)
        self.staff.append(s)

    def getPersonnelByName(self, name_):
        for n in self.staff:
            if n.name == name_:
                return n
        return None

    def removePersonnel(self, name_):
        s = self.getPersonnelByName(name_)
        if s is not None:
            self.staff.remove(s)
        return f"{s} has been removed from the hospital staff"
