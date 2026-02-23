import requests
from requests.auth import HTTPDigestAuth

ip = "192.168.1.164"
url = f"http://{ip}/ISAPI/AccessControl/AcsEvent?format=json"
url = f"http://{ip}/ISAPI/AccessControl/UserInfo/Search?format=json"

r = requests.post(url, auth=HTTPDigestAuth("admin", "Iqra@12#"))

print(r.text)
