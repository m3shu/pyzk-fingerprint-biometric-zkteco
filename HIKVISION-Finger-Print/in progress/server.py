from flask import Flask, request, jsonify
import json
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=["POST"])
@app.route("/api/hikvision/event", methods=["POST"])
def receive_event():

    content_type = request.content_type or ""

    result = None

    # -------- MULTIPART --------
    if "multipart" in content_type:

        for key in request.form:
            payload = request.form[key]

            if payload.strip().startswith("{"):
                result = handle_json(payload)

            elif payload.strip().startswith("<"):
                result = handle_xml(payload)

        for file_key in request.files:
            _ = request.files[file_key]  # image if needed

    # -------- JSON --------
    elif request.is_json:
        result = handle_json(request.get_json())

    # -------- RAW --------
    else:
        raw = request.data.decode("utf-8", errors="ignore")

        if raw.strip().startswith("<"):
            result = handle_xml(raw)
        elif raw.strip().startswith("{"):
            result = handle_json(raw)

    # -------- RESPONSE --------
    if result:
        return jsonify({
            "status": "success",
            "message": "Event received",
            "data": result
        }), 200

    return jsonify({
        "status": "ignored",
        "message": "No valid event found"
    }), 200


# ---------------- JSON EVENT ----------------
def handle_json(data):

    if isinstance(data, str):
        data = json.loads(data)

    try:
        event = data.get("Events", {}).get("EventNotification", {})
        access = event.get("AccessControllerEvent", {})

        employee_no = access.get("employeeNoString")
        name = access.get("name")
        verify_mode = access.get("currentVerifyMode")

        # ignore heartbeat / empty events
        if not employee_no:
            return None

        result = {
            "employee": employee_no,
            "name": name,
            "verify_mode": verify_mode,
            "time": datetime.now().isoformat()
        }

        print("\n========== SUCCESS EVENT ==========")
        print(result)
        print("===================================")

        return result

    except Exception as e:
        print("JSON parse error:", e)
        return None


# ---------------- XML EVENT ----------------
def handle_xml(xml_string):

    try:
        root = ET.fromstring(xml_string)

        employee = root.findtext(".//employeeNoString")
        name = root.findtext(".//name")
        verify = root.findtext(".//currentVerifyMode")

        if not employee:
            return None

        result = {
            "employee": employee,
            "name": name,
            "verify_mode": verify,
            "time": datetime.now().isoformat()
        }

        print("\n========== SUCCESS EVENT ==========")
        print(result)
        print("===================================")

        return result

    except Exception as e:
        print("XML parse error:", e)
        return None


if __name__ == "__main__":
    print("Hikvision Event Listener Running on port 5000...")
    app.run(host="0.0.0.0", port=5000)