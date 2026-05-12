# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK

#for setting specific time
today = datetime.today()
nowTime = today.replace(hour=9, minute=58, second=0, microsecond=0)

conn = None
zk = ZK('192.168.1.201', port=4370)
try:
    conn = zk.connect()
    print ("Syncing time...")
    conn.set_time(nowTime)
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
