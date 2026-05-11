import requests
from requests.auth import HTTPDigestAuth

IP = "192.168.68.66"
AUTH = HTTPDigestAuth("admin", "Mollah@26")
BASE = f"http://{IP}"

def configure_http_host():
    payload = {
        "HttpHostNotification": {
            "id": 1,
            "url": "/api/hikvision/event",
            "protocolType": "HTTP",
            "parameterFormatType": "JSON",
            "addressingFormatType": "ipaddress",
            "ipAddress": "192.168.68.62",
            "portNo": 5000,
            "httpAuthType": "none"
        }
    }

    r = requests.put(
        f"{BASE}/ISAPI/Event/notification/httpHosts/1?format=json",
        json=payload,
        auth=AUTH,
        timeout=10
    )

    print("Status:", r.status_code)
    print(r.text)

configure_http_host()