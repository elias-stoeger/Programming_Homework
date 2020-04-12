from flask import Flask, request, jsonify
from CovidManagementSystem import *


app = Flask(__name__)

# Root object for the management system
ms = CovidManagementSystem()


# Add a new hospital (parameters: name, capacity).
@app.route("/hospital", methods=["POST"])
def addHospital():
    try:
        ms.addHospital(request.args.get('name'), request.args.get('capacity'))
        return jsonify(f"Added a new hospital called {request.args.get('name')} with capacity {request.args.get('capacity')}")
    except ValueError:
        return jsonify("Capacity has to be an integer")

# Return the details of a hospital of the given hospital_id.
@app.route("/hospital/<hospital_id>", methods=["GET"])
def hospitalInfo(hospital_id):       
    h = ms.getHospitalById(hospital_id)
    if h is not None:
        return jsonify(h.serialize())
    return jsonify(
            success=False,
            message="Hospital not found")

# Admission of a patient to a given hospital 
@app.route("/hospital/<hospital_id>/patient", methods=["POST"])
def admitPatientToHospital(hospital_id):
    h = ms.getHospitalById(hospital_id)
    if h is not None:
        p = h.admission(request.args.get('name'), request.args.get('dob'))
        return jsonify(
            success=h is not None,
            message=f"Patient {p.name} admitted to {h.name}")
    else:
        return jsonify("No hospital with his ID found.")

#  delete a hospital of given ID
@app.route("/hospital/<hospital_id>", methods=["DELETE"])
def deleteHospital(hospital_id):
    result = ms.deleteHospital(hospital_id)   
    if result:
        message = f"Hospital with id{hospital_id} was deleted" 
    else: 
        message = "Hospital not found" 
    return jsonify(
            success=result,
            message=message)

#  return all your hospitals and some stats
@app.route("/hospitals", methods=["GET"])
def allHospitals():   
    return jsonify(hospitals=[h.serialize() for h in ms.getHospitals()])


@app.route("/quarantine", methods=["POST"])
def addQuarantineArea():
    try:
        ms.addQuarantineArea(request.args.get('name'), request.args.get('capacity'))
        return jsonify(f"Added a new quarantine area called {request.args.get('name')} with capacity {request.args.get('capacity')}")
    except ValueError:
        return jsonify("Capacity has to be an integer")
@app.route("/quarantine/<qu_id>", methods=["GET"])
def QuarantineAreaInfo(qu_id):
    q = ms.getQuarantineAreaByID(qu_id)
    if q is not None:
        return jsonify(q.serialize())
    return jsonify(
        success=False,
        message="Quarantine area not found")

@app.route("/quarantine/<qu_id>/<pat_id>", methods=["POST"])
def admitPatientToQuarantine(qu_id, pat_id):
    q = ms.getQuarantineAreaByID(qu_id)
    p = ms.getPatientByID(pat_id)
    r = ms.getFacilityByPatientID(pat_id)
    if q == r:
        return jsonify("Patient already in this facility")
    elif q is not None and p is not None:
        ms.admitPatient(pat_id, qu_id)
        return jsonify(f"Patient {p.name} admitted to {q.name}")
    elif q is None:
        return jsonify("Quarantine area not found")
    elif p is None:
        return jsonify("Patient not found")
    else:
        return jsonify("Something isn't working")

@app.route("/quarantine/<qu_id>", methods=["DELETE"])
def deleteQuarantineArea(qu_id):
    p = ms.deleteQuarantineArea(qu_id)
    if p == "No Place":
        return jsonify(p)
    elif p is not None:
        return jsonify(f"Quarantine area with id{qu_id} was deleted")
    else:
        return jsonify("Quarantine area could not be deleted")

@app.route("/quarantines", methods=["GET"])
def allQuarantineAreas():
    return jsonify(quarantines=[q.serialize() for q in ms.getQuarantineAreas()])

@app.route("/staff", methods=["POST"])
def addStaff():
    try:
        p = ms.addPersonnel(request.args.get('name'), request.args.get('dob'), request.args.get('type'))
        return jsonify(f"{p.type} {p.name} added to the system")
    except TypeError:
        return jsonify(f"Staff must either be of type 'doctor' or 'nurse'")

@app.route("/staff", methods=["GET"])
def staffInfo():
    return jsonify(ms.staffStats())

@app.route("/staff/<staff_id>", methods=["PUT"])
def assignStaff(staff_id):
    p = ms.getFacilityByID(request.args.get('workplace'))
    q = ms.getHospitals()
    r = ms.getQuarantineAreas()
    s = ms.getPersonnelByID(staff_id)
    if p is None:
        message = "No facility with the given ID found"
        return jsonify(message)
    else:
        if p in q:
            ms.movePersonnelToHospital(s.name, p.ID)
            return jsonify(f"Assignment of {s.name} to {p.name} successful")
        elif p in r:
            ms.movePersonnelToQuarantineArea(s.name, p.ID)
            return jsonify(f"Assignment of {s.name} to {p.name} successful")
        else:
            message = "Error in staff assignment"
            return jsonify(message)

@app.route("/staff/<staff_id>", methods=["DELETE"])
def deleteStaff(staff_id):
    p = ms.getAllStaff()
    allIDs = []
    for q in p:
        allIDs.append(q.ID)
    if staff_id in allIDs:
        s = ms.getPersonnelByID(staff_id)
        for x in ms.hospitals:
            for y in x.staff:
                if s == y:
                    x.staff.remove(y)
                    return jsonify("Target eliminated!")
        for x in ms.quarantine_areas:
            for y in x.staff:
                if s == y:
                    x.staff.remove(y)
                    return jsonify("Target eliminated!")
        for x in ms.unassignedStaff:
            if s == x:
                ms.unassignedStaff.remove(x)
                return jsonify("Target eliminated!")
    else:
        return jsonify("No Personnel with that ID found")

@app.route("/patient", methods=["POST"])
def addPatient():
    h = ms.addPatient(request.args.get('name'), request.args.get('dob'))
    return jsonify(f"Patient {h.name}, born {h.dob} with ID {h.ID} added to the system")

#  for displaying all patients in the system, nice for debugging
@app.route("/patients", methods=["GET"])
def getPatients():
    return jsonify(ms.allPatients())

@app.route("/patient/<pat_id>/admit/<facility_id>", methods=["PUT"])
def admitPatient(pat_id, facility_id):
    p = ms.admitPatient(pat_id, facility_id)
    if p is None:
        return jsonify("Could not admit patient")
    else:
        return jsonify("Patient admitted successfully")

@app.route("/patient/<pat_id>/discharge/<facility_id>", methods=["PUT"])
def dischargePatient(pat_id, facility_id):
    h = ms.dischargePatient(pat_id, facility_id)
    if h is not None:
        return jsonify("Patient discharged")
    return jsonify("Patient could not be discharged")

@app.route("/patient/<pat_id>/diagnosis", methods=["POST"])
def diagnosis(pat_id):
    h = ms.diagnosis(pat_id)
    if h is None:
        return jsonify("Patient was tested positive and moved into quarantine")
    return jsonify("Patient was tested negative and has been discharged from all facilities")

@app.route("/patient/<pat_id>/cure", methods=["POST"])
def cure(pat_id):
    h = ms.cure(pat_id)
    if h is None:
        return jsonify("Patient could not be cured and has fallen victim to the virus, may he rest in peace...")
    return jsonify("Patient was successfully cured and discharged from all facilities")

@app.route("/stats", methods=["GET"])
def totalStats():
    return jsonify(ms.stats())

@app.route("/")
def index():
    return jsonify(
            success=True,
            message="Your server is running! Welcome to the Covid API.")

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE"
    return response


if __name__ == "__main__":
    app.run(debug=False, port=8888)
