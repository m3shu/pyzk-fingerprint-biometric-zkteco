import requests
from requests.auth import HTTPDigestAuth

ip = "192.168.1.164"
url = f"http://{ip}/ISAPI/AccessControl/AcsEvent?format=json"

bodyJson = {
    "AcsEventCond": {
        "searchID": "12345678-1234-1234-1234-123456789012",
        "searchResultPosition": 0,
        "maxResults": 10,
        "major": 5
    }
}

r = requests.post(
    url,
    #data=bodyJson,
    #headers={"Content-Type": "application/xml"},
    auth=HTTPDigestAuth("admin", "Iqra@12#"),
    #timeout=10
)

print(r.text)
