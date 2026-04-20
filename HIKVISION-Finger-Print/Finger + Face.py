import requests
from requests.auth import HTTPDigestAuth

url = "http://192.168.1.165/ISAPI/AccessControl/AcsEvent?format=json"

payload = {
  "AcsEventCond": {
    "searchID": "1",
    "searchResultPosition": 0,
    "maxResults": 100,
    "major": 5,
    "minor": 0, # 0 = all
    #"minor": 38, # 38 = finger
	#"minor": 75, #75 = face
  }
}

r = requests.post(
    url,
    json=payload,
    auth=HTTPDigestAuth("admin", "Iqra@12#"),
    timeout=10
)


data = r.json()["AcsEvent"]["InfoList"]
print(len(data))
counter = 1
print("-"*26+"Finger"+"-"*27)
for e in data:
    if(e["minor"]==38):
        print(f"#{counter} {e['time']} ==> {e['cardReaderNo']} ===> {e['name']}")
        counter+=1


counter = 1
print("-"*27+"Face"+"-"*28)
for e in data:
    if(e["minor"]==75):
        print(f"#{counter} {e['time']} ==> {e['cardReaderNo']} ===> {e['name']}")
        counter+=1        