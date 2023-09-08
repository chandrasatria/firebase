

import datetime

def strToDate(date):
	date = str(date)
	if len(date)>=10:
		date = date[:10]
	t = datetime.datetime.strptime(date,"%Y-%m-%d")
	return t