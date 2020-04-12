import uuid


class Staff:
    def __init__(self, name, dob, type_):
        self.ID = str(uuid.uuid1())
        self.dob = dob
        self.name = name
        self.type = type_
        self.check()

    def check(self):
        tests = ["doctor", "nurse"]
        if self.type in tests:
            pass
        else:
            raise TypeError(f"{self.type}Type must be either \"doctor\" or \"nurse\"")
