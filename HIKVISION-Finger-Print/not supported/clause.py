import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
from datetime import datetime
import json

class HikvisionAttendance:
    def __init__(self, ip_address, username, password, port=80):
        """
        Initialize connection to HIKVISION device
        
        Args:
            ip_address: Device IP address
            username: Device username (default: admin)
            password: Device password
            port: HTTP port (default: 80)
        """
        self.base_url = f"http://{ip_address}:{port}/ISAPI"
        self.auth = HTTPDigestAuth(username, password)
        self.session = requests.Session()
        
    def get_attendance_records(self, start_time=None, end_time=None, search_id="1"):
        """
        Get attendance/access control records
        
        Args:
            start_time: Start time (format: "2024-01-01T00:00:00")
            end_time: End time (format: "2024-01-27T23:59:59")
            search_id: Search ID (default: "1")
        """
        url = f"{self.base_url}/AccessControl/AcsEvent"
        
        # Build XML request
        if start_time and end_time:
            xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
            <AcsEventCond>
                <searchID>{search_id}</searchID>
                <searchResultPosition>0</searchResultPosition>
                <maxResults>100</maxResults>
                <major>0</major>
                <minor>0</minor>
                <startTime>{start_time}</startTime>
                <endTime>{end_time}</endTime>
            </AcsEventCond>"""
        else:
            # Get recent records
            xml_data = """<?xml version="1.0" encoding="UTF-8"?>
            <AcsEventCond>
                <searchID>1</searchID>
                <searchResultPosition>0</searchResultPosition>
                <maxResults>100</maxResults>
            </AcsEventCond>"""
        
        headers = {
            'Content-Type': 'application/xml',
        }
        
        try:
            response = self.session.post(
                url,
                data=xml_data,
                auth=self.auth,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return self.parse_attendance_data(response.content)
            else:
                print(f"Error: Status code {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return None
    
    def parse_attendance_data(self, xml_content):
        """Parse XML response and extract attendance records"""
        try:
            root = ET.fromstring(xml_content)
            records = []
            
            # Parse each InfoList entry
            for info in root.findall('.//InfoList'):
                record = {}
                
                # Extract employee info
                employee = info.find('employeeNoString')
                if employee is not None:
                    record['employee_no'] = employee.text
                
                # Extract name
                name = info.find('name')
                if name is not None:
                    record['name'] = name.text
                
                # Extract time
                time_elem = info.find('time')
                if time_elem is not None:
                    record['time'] = time_elem.text
                
                # Extract card number
                card = info.find('cardNo')
                if card is not None:
                    record['card_no'] = card.text
                
                # Extract door/reader info
                door = info.find('doorNo')
                if door is not None:
                    record['door_no'] = door.text
                
                # Extract event type (entry/exit)
                event_type = info.find('major')
                if event_type is not None:
                    record['event_type'] = event_type.text
                
                records.append(record)
            
            return records
            
        except Exception as e:
            print(f"Error parsing XML: {str(e)}")
            return None
    
    def get_all_employees(self):
        """Get list of all employees"""
        url = f"{self.base_url}/AccessControl/UserInfo/Search"
        
        xml_data = """<?xml version="1.0" encoding="UTF-8"?>
        <UserInfoSearchCond>
            <searchID>1</searchID>
            <searchResultPosition>0</searchResultPosition>
            <maxResults>100</maxResults>
        </UserInfoSearchCond>"""
        
        headers = {'Content-Type': 'application/xml'}
        
        try:
            response = self.session.post(
                url,
                data=xml_data,
                auth=self.auth,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"Error getting employees: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Exception: {str(e)}")
            return None


# Example usage
if __name__ == "__main__":
    # Device configuration
    DEVICE_IP = "192.168.1.164"  # Change to your device IP
    USERNAME = "admin"
    PASSWORD = "Iqra@12#"  # Change to your password
    
    # Create instance
    device = HikvisionAttendance(DEVICE_IP, USERNAME, PASSWORD)
    
    # Get today's attendance records
    today = datetime.now().strftime("%Y-%m-%dT00:00:00")
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    print(f"Fetching attendance records from {today} to {now}...")
    records = device.get_attendance_records(start_time=today, end_time=now)
    
    if records:
        print(f"\nFound {len(records)} records:\n")
        for i, record in enumerate(records, 1):
            print(f"Record {i}:")
            print(f"  Employee No: {record.get('employee_no', 'N/A')}")
            print(f"  Name: {record.get('name', 'N/A')}")
            print(f"  Time: {record.get('time', 'N/A')}")
            print(f"  Card No: {record.get('card_no', 'N/A')}")
            print(f"  Door No: {record.get('door_no', 'N/A')}")
            print()
    else:
        print("No records found or error occurred")
    
    # Optional: Save to JSON file
    if records:
        with open('attendance_records.json', 'w') as f:
            json.dump(records, f, indent=2)
        print("Records saved to attendance_records.json")