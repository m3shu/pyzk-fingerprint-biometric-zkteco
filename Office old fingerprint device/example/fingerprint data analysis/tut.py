import json
from datetime import datetime
text = open("abc.txt").read()
punchList = json.loads(text)
#print(len(a))
#print(a)
today = datetime.now().strftime("%Y-%m-%d")
#print(today)
#quit()
for punch in punchList:
	#print(punch)
	userId = punch['UserId']
	#print(userId)
	date = punch['Time'][:10]
	if(date==today):
		print(userId)
	#print(date)

	