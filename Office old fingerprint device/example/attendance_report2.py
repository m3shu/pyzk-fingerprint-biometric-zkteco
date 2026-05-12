import json
from zk import ZK

def FormatData(data):
	data = data.replace("[","")
	data = data.replace("]","")
	data = data.replace("<Attendance>: ","")
	data = data.strip()
	data = data.split("),")

	userData = []
	for d in data:
		userId = int(d.split(":")[0])
		time = ":".join(d.split("(")[0].split(":")[1:]).strip()
		userData.append({"UserId":userId,"Time":time})

	userData = json.dumps(userData)		
	return userData

def GetAttendance(ip,portNo):
	ip = str(ip)
	portNo = int(portNo)
	conn = None
	zk = ZK(ip, port=portNo)
	try:
	    conn = zk.connect()	    
	    return FormatData(str(conn.get_attendance()))
	except Exception as e:
	    return "Process terminate : {}".format(e)
	finally:
	    if conn:
	        conn.disconnect()

if(__name__=="__main__"):
	#ip,portNo = input("Enter ip and port: ").split(" ")
	ip,portNo = "192.168.1.201","4370"
	print(GetAttendance(ip,portNo))