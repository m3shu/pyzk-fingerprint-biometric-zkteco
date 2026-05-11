import requests
from requests.auth import HTTPDigestAuth

IP = "192.168.68.66"
url = f"http://{IP}/ISAPI/AccessControl/AcsEvent?format=json"

payload = {
  "AcsEventCond": {
    "searchID": "1",
    "searchResultPosition": 0,
    "maxResults": 100,
    "major": 5,
    #"minor": 38, #for finger
	"minor": 75, #for face
  }
}

r = requests.post(
    url,
    json=payload,
    auth=HTTPDigestAuth("admin", "Mollah@26"), #Iqra@12#
    timeout=10
)


counter = 1
data = r.json()["AcsEvent"]["InfoList"]
for e in data:
    print(f"#{counter} {e['time']} ==> {e['cardReaderNo']} ===> {e['name']}")
    counter+=1