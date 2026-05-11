import requests
import time
import json
from requests.auth import HTTPDigestAuth

IP = "192.168.68.66"
AUTH = HTTPDigestAuth("admin", "Mollah@26")
BASE = f"http://{IP}"

def get(path):
    return requests.get(f"{BASE}{path}", auth=AUTH, timeout=10)

def post(path, payload):
    return requests.post(f"{BASE}{path}", json=payload, auth=AUTH, timeout=10)

# ── STEP 1: Check if device supports fingerprint capture ──────────────────────
def check_capability():
    r = get("/ISAPI/AccessControl/capabilities")
    print("Capabilities:", r.status_code)
    if "isSupportCaptureFingerPrint" in r.text:
        print("✓ Device supports fingerprint capture")
        return True
    else:
        print("✗ Device may NOT support fingerprint capture")
        print(r.text)
        return False

# ── STEP 2: Trigger capture (user must place finger on scanner NOW) ───────────
def start_capture(employee_no, finger_id=1, card_reader_no=1):
    """
    fingerPrintID: 1–10 (which finger slot to store in)
    cardReaderNo:  usually 1 (the built-in reader)
    """
    payload = {
        "CaptureFingerPrintCond": {
            "employeeNo": str(employee_no),
            "fingerPrintID": finger_id,
            "cardReaderNo": card_reader_no
        }
    }
    r = post("/ISAPI/AccessControl/CaptureFingerPrint?format=json", payload)
    print(f"Capture trigger: {r.status_code}")
    print(r.text)
    return r.status_code == 200

# ── STEP 3: Poll for result ───────────────────────────────────────────────────
def poll_capture_result(timeout=30):
    """
    Keeps polling every second until fingerprint is captured or timeout reached.
    Returns the fingerprint data dict if successful, None otherwise.
    """
    print("Waiting for finger placement", end="", flush=True)
    
    for _ in range(timeout):
        r = get("/ISAPI/AccessControl/CaptureFingerPrint/Status?format=json")
        
        if r.status_code == 200:
            try:
                data = r.json()
                status = data.get("CaptureFingerPrintStatus", {})
                state = status.get("status", "")  # "capturing", "success", "failed"
                
                if state == "success":
                    print("\n✓ Fingerprint captured!")
                    print(f"  Quality score : {status.get('fingerPrintQuality')}")
                    print(f"  Finger ID     : {status.get('fingerPrintID')}")
                    # fingerPrintData contains the base64-encoded template
                    fp_data = status.get("fingerPrintData")
                    return fp_data
                
                elif state == "failed":
                    print(f"\n✗ Capture failed: {status.get('errorCode')}")
                    return None
                    
            except Exception as e:
                print(f"\nParse error: {e} | Raw: {r.text}")
        
        print(".", end="", flush=True)
        time.sleep(1)
    
    print("\n✗ Timeout — no finger detected")
    return None

# ── STEP 4 (optional): Save fingerprint to the person's profile ───────────────
def save_fingerprint(employee_no, finger_id, fp_data_base64):
    payload = {
        "FingerPrintCfg": {
            "employeeNo": str(employee_no),
            "fingerPrintID": finger_id,
            "fingerPrintData": fp_data_base64,
            "deleteFingerPrint": False
        }
    }
    r = post("/ISAPI/AccessControl/FingerPrint/SetUp?format=json", payload)
    print(f"Save fingerprint: {r.status_code} | {r.text}")

# ── MAIN FLOW ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    EMPLOYEE_NO = "1001"   # change to your employee ID
    FINGER_ID   = 1        # 1=right thumb, 2=right index, etc.

    if check_capability():
        input(f"\nPress Enter, then place finger on scanner for employee {EMPLOYEE_NO}...")
        
        if start_capture(EMPLOYEE_NO, finger_id=FINGER_ID):
            fp_data = poll_capture_result(timeout=30)
            
            if fp_data:
                save_fingerprint(EMPLOYEE_NO, FINGER_ID, fp_data)
                print("\nDone! Fingerprint enrolled.")