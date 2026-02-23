from zk import ZK, const

conn = None

zk = ZK(
    '192.168.10.202',
    port=4370,
    timeout=5,
    password=12345
)

try:
    conn = zk.connect()
    conn.disable_device()   # 🔴 IMPORTANT

    # Check existing users
    users = conn.get_users()
    for user in users:
        if user.user_id == '5':
            print("User already exists, deleting first...")
            conn.delete_user(uid=user.uid)

    # Add new user
    conn.set_user(
        uid=5,
        name='Meshu',
        privilege=const.USER_DEFAULT,
        password='12345',
        user_id='5'
    )

    print("User added successfully")

    conn.enable_device()   # 🟢 Re-enable device

except Exception as e:
    print("Process terminate :", e)

finally:
    if conn:
        conn.disconnect()
