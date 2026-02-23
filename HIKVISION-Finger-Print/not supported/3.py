import requests
from requests.auth import HTTPDigestAuth

ip = "192.168.1.164"
url = f"http://{ip}/ISAPI/AccessControl/AcsEvent/Search"

xml = """<?xml version="1.0" encoding="utf-8"?>
<AcsEventCond>
    <searchID>1</searchID>
    <searchResultPosition>0</searchResultPosition>
    <maxResults>10</maxResults>
</AcsEventCond>
"""

r = requests.post(
    url,
    data=xml,
    headers={"Content-Type": "application/xml"},
    auth=HTTPDigestAuth("admin", "Iqra@12#"),
    timeout=10
)

print(r.status_code)
print(r.text)
