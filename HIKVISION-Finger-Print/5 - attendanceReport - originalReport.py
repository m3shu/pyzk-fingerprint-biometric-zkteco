import requests

url = "http://192.168.1.164/doc/index.html#/attendanceReport/originalReport"
#url = "http://192.168.1.164/ISAPI/Security/sessionHeartbeat"


cookies = {
    "WebSession_05070B90EA": "ec680e3952cf7dffc78f8187fe4a4b617467cbe9c94930c3b7be9d38769f5dfa",    
}

response = requests.get(url, cookies=cookies)


print("Status code:", response.status_code)
print("Response body:", response.text)
