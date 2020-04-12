from Hospital import *
from Quarantine import *
from Personnel import *
from Patient import *
import random


class CovidManagementSystem:
    def __init__(self):
        self.hospitals = []  # list of hospitals known to the system
        self.quarantine_areas = []  # list of quarantine areas known to the system
        self.unassignedStaff = []  # list of staff not currently assigned to any facility
        self.unassignedPatients = []  # list of patients not currently assigned to any facility
        self.corpses = []  # for ethnic reasons, this is a list of patients that died.
                           # they are still known to the system but unavailable for tests

    def getHospitals(self):
        return self.hospitals

    def addHospital(self, name, capacity):
        h = Hospital(name, capacity)
        self.hospitals.append(h)
    
    def getHospitalById(self, id_): 
        for h in self.hospitals: 
            if h.ID == id_:
                return h
        return None 
    
    def deleteHospital(self, id_):
        h = self.getHospitalById(id_)
        if h is not None:
            self.hospitals.remove(h)
        return h is not None

    # For showing the hospitals and their status in percentage and absolute numbers
    def getHospitalStats(self):
        stats = []
        for h in self.hospitals:
            stats.append(f"{h.name} is {h.occupancy()}% full, that means {len(h.patients)} beds are taken "
                         f"and {h.capacity - len(h.patients)} are free\n")
        return stats

    # for showing the quarantine areas and their status in percentage and absolute numbers
    def getQuarantineStats(self):
        stats = []
        for q in self.quarantine_areas:
            stats.append(f"{q.name} is {q.occupancy()}% full, that means {len(q.patients)} beds are taken "
                         f"and {q.capacity - len(q.patients)} are free\n")
        return stats

    def getQuarantineAreas(self):
        return self.quarantine_areas

    def addQuarantineArea(self, name, capacity):
        q = quarantine(name, capacity)
        self.quarantine_areas.append(q)

    def getQuarantineAreaByID(self, id_):
        for q in self.quarantine_areas:
            if q.ID == id_:
                return q
        return None

    def deleteQuarantineArea(self, id_):
        q = self.getQuarantineAreaByID(id_)
        t = []
        for x in self.quarantine_areas:
            t.append(x)
        if q is not None:
            if len(q.patients) > 0 and len(t) > 1:
                while t != [] or len(q.patients) > 0:
                    if int(t[0].capacity) - len(t[0].patients) - len(q.patients) >= 0:
                        for y in q.patients:
                            t[0].patients.append(y)
                            q.patients.remove(y)
                    else:
                        t.remove(t[0])
                if len(q.patients) == 0:
                    return not None
                else:
                    return None
            elif len(q.patients) > 0 and len(t) < 2:
                return "No Place"
            elif len(q.patients) == 0:
                self.quarantine_areas.remove(q)
                return not None
            else:
                return None
        else:
            return None

    def addPersonnel(self, name, dob, type_):
            p = Staff(name, dob, type_)
            self.unassignedStaff.append(p)
            return p

    def getPersonnelByName(self, name):
        for x in self.hospitals and self.quarantine_areas:
            for n in x.name:
                if name == n:
                    return n
                else:
                    return None

    def movePersonnelToHospital(self, name_staff, ID):
        if self.getPersonnelByName(name_staff) is not None:
            p = self.getPersonnelByName(name_staff)
        else:
            return None
        if self.getHospitalById(ID) is not None:
            n = self.getHospitalById(ID)
        else:
            return None
        for h in self.hospitals:
            if p in h.staff:
                h.staff.remove(p)
        for h in self.quarantine_areas:
            if p in h.staff:
                h.staff.remove(p)
        n.append(p)
        return f"Staff member {p} moved to {n.name}"

    def movePersonnelToQuarantineArea(self, name_staff, ID):
        if self.getPersonnelByName(name_staff) is not None:
            p = self.getPersonnelByName(name_staff)
        else:
            return "No Personnel with the given name found in the system"
        if self.getQuarantineAreaByID(ID) is not None:
            n = self.getQuarantineAreaByID(ID)
        else:
            return "ID not found in the system"
        for q in self.quarantine_areas:
            if p in q.staff:
                q.staff.remove(q)
        n.append(p)
        return f"Staff member {p} moved to {n.name}"

    def movePatientToQuarantineArea(self, pat_ID):
        if self.getPatientByID(pat_ID) is not None:
            p = self.getPatientByID(pat_ID)
        else:
            return "No Patient with the given ID found in the system"
        q_areas = random.shuffle(self.quarantine_areas)
        q = None
        while q is None and len(q_areas) > 0:
            if q_areas[0].capacity - len(q_areas[0].patients) > 0:
                q = q_areas[0]
            else:
                del q_areas[0]
        if q is None:
            return "No Quarantine Area with enough room found in the system"
        else:
            q.patients.append(p)
            return f"Patient {p.name} moved to {q.name}"

    def getPatientByID(self, pat_ID):
        for p in self.hospitals:
            for q in p.patients:
                if q.ID == pat_ID:
                    return q
        for p in self.quarantine_areas:
            for q in p.patients:
                if q.ID == pat_ID:
                    return q
        for p in self.unassignedPatients:
            if p.ID == pat_ID:
                return p
        return None

    def getFacilityByPatientID(self, pat_ID):
        for p in self.hospitals:
            for q in p.patients:
                if q.ID == pat_ID:
                    return p
        for p in self.quarantine_areas:
            for q in p.patients:
                if q.ID == pat_ID:
                    return p
        return None

    def diagnosis(self, pat_ID):
        # in the diagnosis, patients have a 10% chance to be diagnosed as positive
        luckyNumber = random.randint(1, 10)
        if luckyNumber > 1:
            newStatus = "negative"
        else:
            newStatus = "positive"
        patient = self.getPatientByID(pat_ID)
        patient.status = newStatus
        if newStatus == "negative":
            facility = self.getFacilityByPatientID(pat_ID)
            if facility is None:
                return not None
            else:
                facility.removePatient(patient.name)
            return not None
        else:
            self.movePatientToQuarantineArea(pat_ID)
            return None

    def cure(self, pat_ID):
        patient = self.getPatientByID(pat_ID)
        facility = self.getFacilityByPatientID(pat_ID)
        luckyNumber = random.randint(1, 100)
        if luckyNumber <= 97:
            if facility is None:
                patient.status = "cured"
            else:
                patient.status = "cured"
                self.unassignedPatients.append(patient)
                facility.patients.remove(patient)
            return not None
        else:
            self.corpses.append(patient)
            facility.patients.remove(patient)
            patient.status = "deceased"
            return None

    def stats(self):
        Inf = 0
        notInf = 0
        Patient_stats = {}
        for h in self.hospitals:
            for p in h.patients:
                Patient_stats[p.name] = p.status
                if p.status == "positive":
                    Inf += 1
                else:
                    notInf += 1
        for h in self.quarantine_areas:
            for p in h.patients:
                Patient_stats[p.name] = p.status
                if p.status == "positive":
                    Inf += 1
                else:
                    notInf += 1
        for h in self.unassignedPatients:
            Patient_stats[h.name] = h.status
        for h in self.corpses:
            Patient_stats[h.name] = h.status
        if Inf + notInf != 0:
            Percentage_Infected = 100 * (Inf / (Inf + notInf))
        else:
            Percentage_Infected = 0
        facility_Stats = {}
        for h in self.hospitals and self.quarantine_areas:
            facility_Stats[h.name] = f"{h.occupancy}%"
        full_stats = {
            "Percentage of infected patients": f"{Percentage_Infected}%",
            "Stats about the facilities": facility_Stats,
            "Patient status": Patient_stats,
        }
        return full_stats

    def staffStats(self):
        staff = {}
        for p in self.hospitals:
            for q in p.staff:
                staff[f"{q.name} / {q.ID}"] = p.name
        for p in self.quarantine_areas:
            for q in p.staff:
                staff[f"{q.name} / {q.ID}"] = p.name
        for p in self.unassignedStaff:
            staff[f"{p.name} / {p.ID}"] = "unassigned"
        return staff

    def getFacilityByID(self, id_):
        p = self.getHospitalById(id_)
        q = self.getQuarantineAreaByID(id_)
        if p is not None:
            return p
        else:
            if q is not None:
                return q
            else:
                return None

    def getAllStaff(self):
        allStaff = []
        for p in self.hospitals:
            for q in p.staff:
                allStaff.append(q)
        for p in self.quarantine_areas:
            for q in p.staff:
                allStaff.append(q)
        for p in self.unassignedStaff:
            allStaff.append(p)
        return allStaff

    def addPatient(self, name, dob):
        p = Patient(name, dob)
        self.unassignedPatients.append(p)
        return p

    def getAllFacilities(self):
        return self.hospitals + self.quarantine_areas

    def admitPatient(self, pat_id, facility_id):
        r = self.getFacilityByID(facility_id)
        s = self.getPatientByID(pat_id)
        t = self.getFacilityByPatientID(pat_id)
        if t is not None:
            t.patients.remove(s)
            r.patients.append(s)
            return not None
        elif s is None:
            return None
        elif r is None:
            return None
        else:
            r.patients.append(s)
            return not None

    def dischargePatient(self, pat_id, facility_id):
        r = self.getFacilityByID(facility_id)
        s = self.getPatientByID(pat_id)
        t = self.getFacilityByPatientID(pat_id)
        if t == r and s is not None and r is not None:
            t.patients.remove(s)
            return not None
        else:
            return None

    def getPersonnelByID(self, staff_id):
        for p in self.hospitals:
            for q in p.staff:
                if q.ID == staff_id:
                    return q
        for p in self.quarantine_areas:
            for q in p.staff:
                if q.ID == staff_id:
                    return q
        for p in self.unassignedStaff:
            if p.ID == staff_id:
                return p

    def allPatients(self):
        pats = {}
        for p in self.unassignedPatients:
            pats[p.name] = p.ID
        for h in self.hospitals:
            for q in h.patients:
                pats[q.name] = q.ID
        for p in self.quarantine_areas:
            for q in p.patients:
                pats[q.name] = q.ID
        return pats

    def unassigned(self):
        pat = {}
        for p in self.unassignedPatients:
            pat[p.name] = p.ID
        return pat
