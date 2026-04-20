import requests
from requests.auth import HTTPDigestAuth

url_user = "http://192.168.1.165/ISAPI/AccessControl/UserInfo/Search?format=json"

payload_user = {
  "UserInfoSearchCond": {
    "searchID": "1",
    "searchResultPosition": 0,
    "maxResults": 100
  }
}

u = requests.post(
    url_user,
    json=payload_user,
    auth=HTTPDigestAuth("admin","Iqra@12#")
)

print(u.json())