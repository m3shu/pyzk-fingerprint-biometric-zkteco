from flask import Flask, request, jsonify
import json
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)


# ==============================
# MAIN ROUTE
# ==============================
@app.route("/", methods=["POST"])
@app.route("/api/hikvision/event", methods=["POST"])
def receive_event():

    content_type = request.content_type or ""

    print("\n==============================")
    print("HIKVISION EVENT RECEIVED")
    print("Content-Type:", content_type)
    print("==============================")

    raw = request.data.decode("utf-8", errors="ignore")

    # DEBUG LOG (VERY IMPORTANT for Hikvision)
    print("RAW BODY:\n", raw)
    print("FORM:", dict(request.form))
    print("FILES:", list(request.files.keys()))
    print("==============================")

    result = None

    # ==============================
    # JSON (direct)
    # ==============================
    if request.is_json:
        result = handle_json(request.get_json())

    # ==============================
    # XML (direct or raw)
    # ==============================
    elif raw.strip().startswith("<"):
        result = handle_xml(raw)

    # ==============================
    # JSON (raw fallback)
    # ==============================
    elif raw.strip().startswith("{"):
        result = handle_json(raw)

    # ==============================
    # MULTIPART FORM
    # ==============================
    elif "multipart" in content_type:

        for key in request.form:

            payload = request.form[key]

            payload = payload.strip()

            if payload.startswith("{"):
                result = handle_json(payload)

            elif payload.startswith("<"):
                result = handle_xml(payload)

    # ==============================
    # RESPONSE
    # ==============================
    if result:
        print("✅ EVENT SUCCESS:", result)

        return jsonify({
            "status": "success",
            "message": "Valid Hikvision event received",
            "data": result
        }), 200

    else:
        print("⚠️ No valid event detected (heartbeat or unknown format)")

        return jsonify({
            "status": "ignored",
            "message": "No valid event found"
        }), 200


# ==============================
# JSON HANDLER
# ==============================
def handle_json(data):

    try:
        if isinstance(data, str):
            data = json.loads(data)

        # Hikvision structure (varies by firmware)
        event = data.get("Events") or data.get("event") or {}

        access = event.get("EventNotification", {}).get("AccessControllerEvent", {})

        employee = access.get("employeeNoString")

        # Ignore heartbeat / empty events
        if not employee:
            print("⚠️ Ignored JSON (heartbeat or empty)")
            return None

        result = {
            "employee": employee,
            "name": access.get("name"),
            "verify_mode": access.get("currentVerifyMode"),
            "time": datetime.now().isoformat()
        }

        print("✅ JSON EVENT:", result)

        return result

    except Exception as e:
        print("❌ JSON ERROR:", e)
        return None


# ==============================
# XML HANDLER
# ==============================
def handle_xml(xml_string):

    try:
        root = ET.fromstring(xml_string)

        employee = root.findtext(".//employeeNoString")

        # Ignore heartbeat
        if not employee:
            print("⚠️ Ignored XML (heartbeat or empty)")
            return None

        result = {
            "employee": employee,
            "name": root.findtext(".//name"),
            "verify_mode": root.findtext(".//currentVerifyMode"),
            "time": datetime.now().isoformat()
        }

        print("✅ XML EVENT:", result)

        return result

    except Exception as e:
        print("❌ XML ERROR:", e)
        return None


# ==============================
# RUN SERVER
# ==============================
if __name__ == "__main__":
    print("🚀 Hikvision Listener Running on port 5000...")
    app.run(host="0.0.0.0", port=5000)