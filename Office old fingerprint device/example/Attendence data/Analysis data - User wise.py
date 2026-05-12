import json
data = open("attendence.txt").read()
data = json.loads(data)



myAttendence = [x for x in data["Attendance"] if(x["UserId"]==5)] #5 = Meshu
#print(myAttendence)

for attendence in myAttendence:
	print(attendence["Time"])
#print(data["Users"])
