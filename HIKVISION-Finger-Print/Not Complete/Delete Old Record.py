import requests
from requests.auth import HTTPDigestAuth

IP = "192.168.68.66"
AUTH = HTTPDigestAuth("admin", "Mollah@26")

def fetch_access_events():
    url = f"http://{IP}/ISAPI/AccessControl/AcsEvent?format=json"
    
    payload = {
        "AcsEventCond": {
            "searchID": "1",
            "searchResultPosition": 0,   # required: start offset
            "maxResults": 50,             # required: how many to return
            "major": 0,
            "minor": 0,
            "startTime": "2024-01-01T00:00:00+06:00",
            "endTime": "2025-12-31T23:59:59+06:00"
        }
    }
    
    r = requests.post(url, json=payload, auth=AUTH, timeout=10)
    
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
    return r

def delete_all_events():
    """Separate endpoint for deleting events"""
    url = f"http://{IP}/ISAPI/AccessControl/AcsEvent/Delete?format=json"
    
    payload = {
        "AcsEventDelCond": {
            "searchID": "1"
        }
    }
    
    r = requests.put(url, json=payload, auth=AUTH, timeout=10)
    print(f"Delete Status: {r.status_code}")
    print(f"Delete Response: {r.text}")
    return r

# fetch_access_events()

delete_all_events()