ip, port, communicationKey =  input().split()
port = int(port)

from zk import ZK

from datetime import datetime

zk = ZK(
    ip,
    port=port,
    timeout=10,
    password=communicationKey
)

# zk = ZK(
#     '192.168.10.202',
#     port=4370,
#     timeout=10,
#     password=12345
# )

conn = None

try:
    conn = zk.connect()
    print("Connected to device")

    conn.disable_device()

    print("Getting attendance logs...")
    attendances = conn.get_attendance()

    for att in attendances:
        print(
            f"User ID: {att.user_id} | "
            f"Time: {att.timestamp} | "
            f"Status: {att.status} | "
            f"PUNCH: {att.punch}"
        )

    print(f"\nTotal Records: {len(attendances)}")

    conn.enable_device()

except Exception as e:
    print("Error:", e)

finally:
    if conn:
        conn.disconnect()
