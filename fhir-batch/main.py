"""Editable one off script to batch a series of FHIR requests"""
import json
import requests

SERVER = "https://fhir.isacc.dev.cirg.uw.edu"


def get_patient(id):
    patients_query = '/'.join((SERVER, "fhir", "Patient", str(id)))
    params = {}
    response = requests.get(patients_query, params=params)
    response.raise_for_status()
    patient = response.json()
    assert patient['resourceType'] == 'Patient'
    return patient


def put_patient(patient):
    id = patient["id"]
    assert id
    patients_query = '/'.join((SERVER, "fhir", "Patient", str(id)))
    params = {}
    response = requests.put(patients_query, params=params, json=patient)
    response.raise_for_status()
    patient = response.json()
    assert patient['resourceType'] == 'Patient'
    return patient


def get_patients():
    patients_query = '/'.join((SERVER, "fhir", "Patient"))
    params = {'_count': 1000}  # or better, implement paging
    response = requests.get(patients_query, params=params)
    response.raise_for_status()
    bundle = response.json()
    assert bundle['resourceType'] == 'Bundle'
    for patient in bundle['entry']:
        yield patient


def add_patient_extension(url, patient_generator):
    """Add extension to any Patient on server w/o one with matching system"""
    ext = {"url": "http://isacc.app/time-of-last-unfollowedup-message",
           "valueDateTime": "2073-01-01T00:00:00.0+00:00"}

    for entry in patient_generator():
        full_url = entry['fullUrl']
        pat = entry['resource']
        found = [e for e in pat.get('extension', []) if e['url'] == ext['url']]
        if found:
            print(f"Patient {full_url} already has desired extension")
            continue

        if 'extension' not in pat:
            pat['extension'] = []
        pat['extension'].append(ext)

        # Can't use full_url, as it requires auth - use backdoor to server
        # to commit change
        _, path = full_url.split('fhir/')
        put_path = '/'.join((url, 'fhir', path))
        response = requests.put(put_path, json=pat)
        # print(response.text)
        response.raise_for_status()


def update_patient(patient_id):
    patient = get_patient(patient_id)
    patient["telecom"][0] = {"system": "sms", "value": "2069314378"}
    after = put_patient(patient)
    if after == patient:
        print("no change detected!")

    print(json.dumps(patient))


if __name__ == "__main__":
    #add_patient_extension(url=SERVER, patient_generator=get_patients)
    update_patient(patient_id=491)
