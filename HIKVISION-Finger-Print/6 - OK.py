import requests
from requests.auth import HTTPDigestAuth

DEVICE_IP = "192.168.1.164"
USERNAME = "admin"
PASSWORD = "Iqra@12#"

# ISAPI endpoint for attendance records
# url = f"http://{DEVICE_IP}/ISAPI/Attendance/Record?format=json"
# url = f"http://192.168.1.164/ISAPI/System/deviceInfo"


# not works
url = "http://192.168.1.164/ISAPI/Attendance/Record"
url = "http://192.168.1.164/ISAPI/AccessControl/AcsEvent"
url = "http://192.168.1.164/ISAPI/Event/notification/AcsEvent"
url = "http://192.168.1.164/ISAPI/ContentMgmt/AttendanceRecord/Search"
url = "http://192.168.1.164/ISAPI/AccessControl/AttendanceRecord"
url = "http://192.168.1.164/ISAPI/Smart/AttendanceRecord"
url = "http://192.168.1.164/ISAPI/AccessControl/UserInfo"
url = "http://192.168.1.164/ISAPI/AccessControl/FingerPrint"
url = "http://192.168.1.164/ISAPI/AccessControl/EventLog"
url = "http://192.168.1.164/ISAPI/AccessControl/CardInfo"
url = "http://192.168.1.164/ISAPI/Streaming/channels/1/picture"

# works
url = "http://192.168.1.164/ISAPI/System/deviceInfo"
url = "http://192.168.1.164/ISAPI/AccessControl/UserInfo/Record"
# url = "http://192.168.1.164/ISAPI/System/capabilities"
# url = "http://192.168.1.164/ISAPI/System/time"
# url = "http://192.168.1.164/ISAPI/System/Network/interfaces"




# body ={
# "searchResultPosition":0,
# "maxResults":5,
# "faceLibType":"blackFD",
# "FDID":"1",
# "FPID":"7"
# }



try:
    response = requests.post(url, auth=HTTPDigestAuth(USERNAME, PASSWORD), timeout=10)
    # response.raise_for_status()  # Raise error if request failed

    print(response.text)
    #data = response.json()  # Parse JSON response
    # print(data)
    # print("Attendance Data:")
    # for record in data.get("AttendanceRecord", []):
    #     print(f"Employee ID: {record['employeeNo']}, Time: {record['time']}, Type: {record['type']}")
        
except requests.exceptions.RequestException as e:

    print("Error connecting to device:", e)
    raise
