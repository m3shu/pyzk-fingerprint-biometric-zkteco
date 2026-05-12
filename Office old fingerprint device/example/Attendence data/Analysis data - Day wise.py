import json
data = open("attendence.txt").read()
data = json.loads(data)


from datetime import datetime
today = datetime.today()
formatted_date = today.strftime("%Y-%m-%d")

formatted_date = "2025-04-15"

#quit(formatted_date)
myAttendence = [x for x in data["Attendance"] if(x["Time"][:10]==formatted_date)] #5 = Meshu

#myAttendence = [x for x in data["Attendance"]] #all
#print(myAttendence)

for attendence in myAttendence:
	userId = str(attendence["UserId"])	
	print(attendence["Time"],"===>", data["Users"][userId], attendence)


