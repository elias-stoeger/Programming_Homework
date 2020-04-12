from Patient import *
from Personnel import *
import uuid


class Hospital:
    def __init__(self, name, capacity):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.capacity = int(capacity)
        self.patients = []  # List of patients admitted to the hospital
        self.staff = []  # List of doctors and nurses working in the hospital

    # return the percentage of occupancy of this hospital 
    def occupancy(self):
        if self.capacity != 0:
            return 100 * len(self.patients) / self.capacity
        return 0

    # admit a patient to the hospital of given name and date of birth 
    def admission(self, name, dob):
        p = Patient(name, dob)
        self.patients.append(p)
        return p

    def getPatient(self, name_):
        for p in self.patients:
            if p.name == name_:
                return p
        return None

    def removePatient(self, name_):
        pNames = []
        for patient in self.patients:
            pNames.append(patient.name)
        if name_ in pNames:
            p = self.getPatient(name_)
            self.patients.remove(p)
            return f"Patient {p.name} removed from the system"
        else:
            return f"Patient \"{name_}\" not found in the system"

    def showPatientStatus(self, name_):
        patient = self.getPatient(name_)
        return patient.status
    
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
