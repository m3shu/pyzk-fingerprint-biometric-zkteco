
import json

# -*- coding: utf-8 -*-
import os
import sys

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK

conn = None
zk = ZK('192.168.1.201', port=4370)

def ReportHtml():
	try:
	    conn = zk.connect()
	    result = conn.get_attendance()
	    return str(result)

	    
	except Exception as e:
	    #print ("Process terminate : {}".format(e))
	    return "Process terminate : {}".format(e)
	finally:
	    if conn:
	        conn.disconnect()

def UsersHtml():
	try:
	    conn = zk.connect()
	    result = conn.get_users()
	    return str(result)

	    
	except Exception as e:
	    #print ("Process terminate : {}".format(e))
	    return "Process terminate : {}".format(e)
	finally:
	    if conn:
	        conn.disconnect()	

from flask import Flask
import requests, json

app = Flask(__name__)

@app.route("/report")
def Report():
	return ReportHtml()


@app.route("/users")
def Users():
	return UsersHtml()

@app.route("/live")
def Live():
	return "Server is running"	


if __name__=="__main__":
	app.run()