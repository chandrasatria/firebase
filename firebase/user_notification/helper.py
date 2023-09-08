from datetime import *
import datetime,calendar


# STUB Time related

def strToTime(time):
	time = str(time)
	if "." in time:
		t = datetime.datetime.strptime(time,"%H:%M:%S.%f")
	else:
		t = datetime.datetime.strptime(time,"%H:%M:%S")
	return t.time()

def strToTimedelta(time):
	time = str(time)
	if "." in time:
		t = datetime.datetime.strptime(time,"%H:%M:%S.%f")
	else:
		t = datetime.datetime.strptime(time,"%H:%M:%S")
	delta = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
	return delta

def strToDatetime(dateTime):
	dateTime = str(dateTime)
	if "." in dateTime:
		t = datetime.datetime.strptime(dateTime,"%Y-%m-%d %H:%M:%S.%f")
	else:
		t = datetime.datetime.strptime(dateTime,"%Y-%m-%d %H:%M:%S")
	return t

def strToDate(date):
	date = str(date)
	if len(date)>=10:
		date = date[:10]
	t = datetime.datetime.strptime(date,"%Y-%m-%d")
	return t

def timeDeltaToStr(timedelta):
	# tambah pengecekan if timedelta tidak sesuai harapan
	# tidak error
	if timedelta is None or timedelta == '':
		return None

	seconds = timedelta.total_seconds()
	hours = seconds / 3600
	minutes = (seconds % 3600) / 60
	seconds = seconds % 3600 % 60
	return "{}:{}:{}".format(int(hours),int(minutes),int(seconds))

def getTimeStamp():
	#timestamp
	import time
	ts = float(time.time())
	return ts

def convertTimeStamp(ts):
	st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
	return st

# STUB Random


# SECTION Perulanagan

# STUB Basic function
def getUmurDoctype(doctype, name):
	doc = frappe.get_doc(doctype,name)
	#pastikan fieldnya tanngal mulai, umur, sampai sekarang
	if doc.sampai_sekarang == 1 and doc.mulai_tanggal!=None:
		tahun = age(doc.mulai_tanggal)
		return "{} tahun".format(str(tahun))
	else:
		return doc.umur

def getUmur(tanggal):
#pastikan fieldnya tanngal mulai, umur, sampai sekarang
	if tanggal!=None:
		if isinstance(tanggal, str):
			tanggal = strToDate(tanggal)
		tahun = age(tanggal)
		return "{} tahun".format(str(tahun))
	else:
		return 0

def getUmurYearMonth(tanggal,current_date=""):
	currentDate = datetime.datetime.now()

	if tanggal!=None:
		if isinstance(tanggal, str):
			tanggal = strToDate(tanggal)
		if isinstance(tanggal, datetime.date):
			tanggal = strToDate(tanggal)
			
		

		deadlineDate= tanggal
		daysLeft = deadlineDate - currentDate

		years = ((daysLeft.total_seconds())/(365.242*24*3600))
		yearsInt=int(years)

		months=(years-yearsInt)*12
		monthsInt=int(months)

		days=(months-monthsInt)*(365.242/12)
		daysInt=int(days)

		hours = (days-daysInt)*24
		hoursInt=int(hours)

		minutes = (hours-hoursInt)*60
		minutesInt=int(minutes)

		seconds = (minutes-minutesInt)*60
		secondsInt =int(seconds)

		if(abs(yearsInt)>1):
			ageText = str(abs(yearsInt)) + " tahun"
		elif(abs(yearsInt)==0):
			ageText = ""
		else: 
			ageText = str(abs(yearsInt)) + " tahun"

		if(abs(monthsInt)>0) and (abs(yearsInt)>0):
			ageText += " and "

		if(abs(monthsInt)>1):
			ageText += str(abs(monthsInt)) + " bulan"
		elif(abs(monthsInt)==0):
			ageText += ""
		else:
			ageText += str(abs(monthsInt)) + " bulan"

		if(ageText==""):
			ageText= "0 bulan"
		print('You are {0:d} years, {1:d}  months, {2:d}  days, {3:d}  hours, {4:d} \
		minutes, {5:d} seconds old.'.format(yearsInt,monthsInt,daysInt,hoursInt,minutesInt,secondsInt))
		return ageText

	return 0
	

def week_of_month(dt):
	""" Returns the week of the month for the specified date.
	"""
	if isinstance(dt, str):
		dt = strToDate(dt)
	first_day = dt.replace(day=1)

	dom = dt.day
	adjusted_weekday = first_day.weekday()+1
	if adjusted_weekday == 7:
		adjusted_weekday =0
	adjusted_dom = dom + adjusted_weekday
	return int(ceil(adjusted_dom/7.0))

def week_of_month_bydate(dt):
	first_day = dt.replace(day=1)

	dom = dt.day
	adjusted_dom = dom + first_day.weekday()

	return int(floor(adjusted_dom/7.0))


def add_months(sourcedate, months):
	month = sourcedate.month - 1 + months
	year = sourcedate.year + month // 12
	month = month % 12 + 1
	day = min(sourcedate.day, calendar.monthrange(year,month)[1])
	string = "{}-{}-{}".format(year,month,day)
	return strToDate(string)

def add_days(sourcedate,daysint):
  u = sourcedate
  d = datetime.timedelta(days=daysint)
  t = u + d
  return t

def getEveryDays_total(start_date, end_date, jump=1):
	start_date = "2019-08-08"
	end_date = "2019-09-02"
	if start_date!=None and end_date!=None:
		if isinstance(start_date, str):
			start_date = strToDate(start_date)
		if isinstance(end_date, str):
			end_date = strToDate(end_date)
		daysLeft = abs(start_date - end_date)
		daysLeft = ceil(daysLeft.days/jump)
	return daysLeft

# NOTE Setiap Hari
def getEveryDays_list(start_date, end_date):
	if start_date!=None:
		if isinstance(start_date, str):
			start_date = strToDate(start_date)
	if end_date!=None:
		if isinstance(end_date, str):
			end_date = strToDate(end_date)
	list_item = []
	while start_date<=end_date:
		list_item += {start_date.strftime("%Y-%m-%d")}
		start_date += timedelta(days=1)
		
	return list_item

def converttoEnglishDay(hari):
	"""
	Change Indonesian hari to Day (bahasa to english)
	"""
	hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
	if hari in hari_list:
		if hari == "Senin":
			day = "Monday"
		elif hari == "Selasa":
			day = "Tuesday"
		elif hari == "Rabu":
			day = "Wednesday"
		elif hari == "Kamis":
			day = "Thursday"
		elif hari == "Jumat":
			day = "Friday"
		elif hari == "Sabtu":
			day = "Saturday"
		elif hari == "Minggu":
			day = "Sunday"
		else:
			day = hari
	else:
		day = hari
	
	return day
# NOTE  Parent Function setiap minggu
# converttoEnglishDay, 
def getWeekDays_list(start_date, end_date
	,days #monday, sunday etc.
	):
	if start_date!=None:
		if isinstance(start_date, str):
			start_date = strToDate(start_date)
	if end_date!=None:
		if isinstance(end_date, str):
			end_date = strToDate(end_date)
	days = converttoEnglishDay(days)
	days = {days} 
	#if more than 1 days in case :D
	list_item = []
	step = timedelta(days=1)
	while start_date <= end_date:
		for day in days:
			# print(calendar.day_name[start_date.date().weekday()])
			if day == calendar.day_name[start_date.date().weekday()]:
				list_item += {start_date.strftime("%Y-%m-%d")}
				# print (calendar.day_name[start_date.date()].strftime("%Y/%m/%d"))
		start_date += step
	
	return list_item

def getMonthWeek(start_date, end_date,
		week,# integer 1-5 / -1 last
		 day, #sunday/monday etc.
		 ):
	# start_date = "2019-08-08"
	# end_date = "2019-09-02"
	if start_date!=None:
		if isinstance(start_date, str):
			start_date = strToDate(start_date)
	if end_date!=None:
		if isinstance(end_date, str):
			end_date = strToDate(end_date)
	# get nearest week
	first_day = start_date.replace(day=1)
	dom = start_date.day
	adjusted_dom = dom + first_day.weekday()
	wn = int(ceil(adjusted_dom/7.0))
	return wn

def getlastmonth(any_day):
	next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
	lastdate = next_month - datetime.timedelta(days=next_month.day)
	return week_of_month(lastdate)

# NOTE setiap bulan 
def getMonthWeek_list(start_date, end_date,
		week,# integer 1-5 / -1 last
		 day, #sunday/monday etc.
		 ):
	day = converttoEnglishDay(day)
	if start_date!=None:
			if isinstance(start_date, str):
				start_date = strToDate(start_date)
	if end_date!=None:
		if isinstance(end_date, str):
			end_date = strToDate(end_date)
	list_item = []
	list_item_need_parsed = []
	# f: perbedaan minggu terakhir dan minggu biasa
	if week == -1:
		# minggu terakhir
		while start_date <= end_date:
			next_month = start_date.replace(day=28) + datetime.timedelta(days=4)
			last_day = next_month - datetime.timedelta(days=next_month.day)
			while True:

				date_day = last_day.weekday()
				if(day == calendar.day_name[date_day]):
					if(last_day<end_date):
						list_item.append(last_day.strftime("%Y-%m-%d"))

					break
				else:
					last_day = last_day-timedelta(days=1)
					print(last_day)
			start_date = add_months(last_day,1)

		
	else:
		# minggu 1-5
		weekcheck = week
		
		while True:
			date_day = start_date.weekday()
			if(day == calendar.day_name[date_day]):
				break
			else:
				start_date = start_date+timedelta(days=1)
		count = start_date.month
		inserted = 0
		while start_date <= end_date:
			wom = week_of_month(start_date)

			if count != start_date.month:
				count = start_date.month
				inserted = 0
				list_item_need_parsed=[]

			list_item_need_parsed.append(start_date.strftime("%Y-%m-%d"))

			if len(list_item_need_parsed) >= int(weekcheck) and inserted == 0:
				inserted = 1 
				list_item.append(list_item_need_parsed[int(weekcheck)-1])

			
			print(str(wom) +"----"+ str(start_date) +"----"+ str(weekcheck) +"---"+str(list_item_need_parsed))
			# jika minggu itu tidak memiliki hari = skip
			# if(week == -1):
			# 	weekcheck = getlastmonth(start_date)
		
			# NOTE Code lama dicomment karena jika minggu 1 hanya mengambil week dan day yang sesuai. jadi banyak ngga dapetnya
			# if(str(weekcheck) == str(wom)):
			# 	list_item.append(start_date.strftime("%Y-%m-%d"))
			start_date = start_date+timedelta(days=7)
	return list_item


def getMonthDate_list(start_date, end_date , date):
	list_item = []
	if start_date!=None and end_date!=None:
		if isinstance(start_date, str):
			start_date = strToDate(start_date)
		if isinstance(end_date, str):
			end_date = strToDate(end_date)
		datewhile = date
		while True:
			try:
				new_date = start_date.replace(day=datewhile)
			except:
				datewhile= datewhile-1
			else:
				break
		if(new_date<start_date):
			new_date = add_months(new_date, 1)
			print(new_date)
	if date == 30 or date == 29 or date == 31 :
		next_month = new_date.replace(day=28) + datetime.timedelta(days=4)
		item = next_month - datetime.timedelta(days=next_month.day)
		while new_date <= end_date:
			list_item += {item.strftime("%Y-%m-%d")}
			new_date = add_months(new_date,1)
			next_month = new_date.replace(day=28) + datetime.timedelta(days=4)
			item = next_month - datetime.timedelta(days=next_month.day)
	else:
		while new_date <= end_date:
			list_item += {new_date.strftime("%Y-%m-%d")}
			new_date = add_months(new_date,1)
	return list_item


def get_repeatable_date(date_start, # use string yyyy-mm-dd or date
						date_end, # use string yyyy-mm-dd or date
						repeat_type, #Setiap hari || Mingguan || Bulanan (string)
						pilihan_perulangan = "",
						hari = "",
						minggu_ke = "", # minggu terakhir = -1
						tanggal = ""# hari terakhir = -1
						):
	'''
	Return json of date
	'''
	if isinstance(date_start, str):
		date_start = strToDate(date_start)
	if isinstance(date_end, str):
		date_end = strToDate(date_end)
	if(repeat_type == "Setiap hari"):
		delta = date_start - date_end
		# jumlah hari
		
	elif (repeat_type == "Mingguan"):
		return True
	elif (repeat_type == "Bulanan"):
		return True
	
	if (delta>100):
		frappe.throw("maximum length is 100")
	else:
		frappe.throw("ok")

# !SECTION

def log_cronjob(method=""):
	try:
		f = open("log_cronjob.txt", "a")
		f.write(str(method)+":"+str(frappe.utils.now())+"\n")
		f.close()
	except:
		pass

import frappe
@frappe.whitelist(allow_guest=True)
def get_complete_url():
	from frappe.utils import cstr
	# Ini ketika ada firebase setting yang site url maka kita pake itu aja
	firebase_setting = frappe.get_single("Firebase Setting")
	if firebase_setting.get("site_url"):
		site_url = firebase_setting.get("site_url")
		if site_url[:-1] == "/":
			site_url = site_url[-1:]
		return site_url
	# Dan ketika site url tidak ada maka kita buat url sendiri
	# Ini ada bug ketika yang jalanin cronjob kluarnya nama site: site1.local misal
	else:
		site_name = cstr(frappe.local.site)
		base_url = frappe.utils.get_url()
		if site_name:
			url_port = frappe.get_conf(site_name).nginx_port
			if url_port:
				return base_url+":"+str(url_port)
			else:
				return base_url
		else:
			return base_url
	
def check_and_append_url_image(url_image):
	# Ini di cek apakah file image yang ada dari frappe yang diupload atau dari url luar
	# Jika false artinya pakai url luar
	check = False
	if '/files/' in url_image[:7]:
		check = True

	
	if check == False:
		return ""
	else:
		return get_complete_url()
	