import requests
from requests.auth import HTTPDigestAuth


url = "http://192.168.1.164/ISAPI/AccessControl/AcsEvent/Search"

#url = "http://192.168.1.164/ISAPI/AccessControl/LocalAttendance/SearchRecordSheet"

r = requests.get(
    url,
    auth=HTTPDigestAuth("admin", "Iqra@12#")
)

print(r.text)
