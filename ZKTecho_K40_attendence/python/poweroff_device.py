from zk import ZK

conn = None

zk = ZK(
    '192.168.10.202',
    port=4370,
    timeout=5,
    password=12345
)

try:
    conn = zk.connect()
    print ("Shutdown the device...")
    conn.poweroff()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
