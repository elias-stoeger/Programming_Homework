import uuid


class Patient:
    def __init__(self, name, dob):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.dob = dob
        self.status = "not yet diagnosed"
