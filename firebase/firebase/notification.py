import frappe
import json
from frappe import _

from firebase.firebase.error import error_result
from frappe.utils import get_request_session
from firebase.firebase.topic import _get_topic
from firebase.firebase.log import log_notification_success, log_notification_failed


#FCM URL
url = "https://fcm.googleapis.com/fcm/send"

#Private Function: Return Server Key FCM
def get_auth_key():
	return frappe.get_value("Firebase Setting","Firebase Setting","server_key")




"""platform (select one) : android, ios, flutter , web
	target_notification (select one)  : User, Global
	notification berbentuk dict {}
	data berbentuk dict {}
	---- optional ---
		user (must be filled when select user)

	contoh notification = {
		"title" : "This is Title",
		"body" : "This is body",
		"badge" : 1,
		"image" : "https://via.placeholder.com/150",
		
	}
	contoh data = {
		"action" : "NOTIFICATION"
	}
	
"""
def send_notification(platform, target_notification, notification={}, data={}, user = ""):
	request_session = get_request_session()
	auth_key,header = get_auth_key_notification_and_header()
	topic = get_topic(target_notification,platform,user = user)
	id = generate_random_id()
	content={
    "to": topic,
    "priority": "high",
    "notification": notification,
    "data": {
        "id": id
    }
	}
	if data:
		content['data'].update(data)
	res = request_session.post(url=url,headers=header,data=json.dumps(content))

	response_code = res.status_code
	if response_code == 200:
		res_json = res.json()
		log_notification_success(response_code=response_code, message_id=res_json.get("message_id"), user=user, topic=topic, title=notification.get("title"), body=notification.get("body"), content=json.dumps(content), data=json.dumps(data), badge=notification.get("badge"), id=id)
	else:
		error = res.text
		log_notification_failed(response_code=response_code, user=user, topic=topic, title=notification.get("title"), body=notification.get("body"), error=error, id=id)
		frappe.throw(error)
	return True

	
	

def get_auth_key_notification_and_header():
	auth_key = get_auth_key()
	if not auth_key:
		frappe.throw(_("Server key has been not set. Please set up on Firebase Settings"))
	header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
	return auth_key,header

def get_topic(target_notification,platform,user=""):
	topic = ""
	if target_notification == "User":
		if not user:
			frappe.throw(_("Please insert the user"))
		topic = "/topics/"+_get_topic(user)
		if not topic:
			frappe.throw(_("Couldn't find user social key"))
	elif target_notification == "Global":
		topic = "/topics/ALL"
	else:
		frappe.throw(_("Topic is invalid"))
	return topic

def generate_random_id():
	from random import randint
	id = str(randint(100000000, 999999999))
	return id




# SECTION Send Notification Basic
#Public Function: Send notification to iOS Devices

def send_notification_ios_badge(user,badge=0):
	title = ""
	body = ""
	s = get_request_session()
	auth_key = get_auth_key()

	if auth_key == "":
		frappe.throw("Server key has been not set")
	else:
		frappe_userid = _get_topic(user)

		if frappe_userid != "": 
			from random import randint
			id = str(randint(100000000, 999999999))
			# id = frappe.utils.now().split(' ')[1].replace(':', '').replace('.', '')

			header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
			topic = "/topics/{}_ios".format(frappe_userid)
			content = {
				"to":topic,
				"notification":{
					# "badge":badge,
					"sound": "default",
					"id": id
				},
				"priority": "high"
			}
			res = s.post(url=url,headers=header,data=json.dumps(content))

			#logging
			response_code = res.status_code
			if response_code == 200:
				res_json = res.json()
				message_id = res_json["message_id"]
				log_notification_success(response_code,message_id,user,topic,title,body,json.dumps(content),badge,id=id)
				# frappe.msgprint("iOS Success notified")
			else:
				error = res.text
				log_notification_failed(response_code,user,topic,title,body,error,id=id)
				frappe.throw(error)
		else:
			frappe.throw("User not found")



"""
	user:String 			-> corresponding to receiver (Link to User)
	title:String 			-> title of the notification
	body:String				-> body of the notification
	badge:Int (optional)	-> badge of the notification
"""
def send_notification_ios(user,title,body,badge=0,action=""):

	s = get_request_session()
	auth_key = get_auth_key()

	if auth_key == "":
		frappe.throw("Server key has been not set")
	else:
		frappe_userid = _get_topic(user)

		if frappe_userid != "": 
			from random import randint
			id = str(randint(100000000, 999999999))
			# id = frappe.utils.now().split(' ')[1].replace(':', '').replace('.', '')

			header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
			topic = "/topics/{}_ios".format(frappe_userid)
			content = {
				"to":topic,
				"notification":{
					"body":body,
					"title":title,
					# "badge":badge,
					"sound": "default",
					"id": id
				},
				"priority": "high"
			}
			if action :
				content["notification"].update({"action":action})
			res = s.post(url=url,headers=header,data=json.dumps(content))

			#logging
			response_code = res.status_code
			if response_code == 200:
				res_json = res.json()
				message_id = res_json["message_id"]
				log_notification_success(response_code,message_id,user,topic,title,body,json.dumps(content),badge,id=id)
				# frappe.msgprint("iOS Success notified")
			else:
				error = res.text
				log_notification_failed(response_code,user,topic,title,body,error,id=id)
				frappe.throw(error)
		else:
			frappe.throw("User not found")


#Public Function: Send notification to Android Devices
"""
	user:String 			-> corresponding to receiver (Link to User)
	title:String 			-> title of the notification
	body:String				-> body of the notification
"""
def send_notification_android(user,title,body,action=""):

	s = get_request_session()
	auth_key = get_auth_key()

	if auth_key == "":
		frappe.throw("Server key has been not set")
	else:
		frappe_userid = _get_topic(user)

		if frappe_userid != "":
			from random import randint
			id = str(randint(100000000, 999999999)) 
			# id = frappe.utils.now().split(' ')[1].replace(':', '').replace('.', '')

			header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
			topic = "/topics/{}_android".format(frappe_userid)
			content = {
				"to":topic,
				"data":{
					"body":body,
					"title":title,
					"id" : id
				}
			}
			if action:
				content['data'].update({"action":action})
			res = s.post(url=url,headers=header,data=json.dumps(content))

			#logging
			response_code = res.status_code
			if response_code == 200:
				res_json = res.json()
				message_id = res_json["message_id"]
				log_notification_success(response_code,message_id,user,topic,title,body,json.dumps(content),id=id)
				# frappe.msgprint("Android Success notified")
			else:
				error = res.text
				log_notification_failed(response_code,user,topic,title,body,error,id=id)
				frappe.throw(error)
		else:
			frappe.throw("User not found")


#Public Function: Send notification to iOS and Android Devices
"""
	user:String 			-> corresponding to receiver (Link to User)
	title:String 			-> title of the notification
	body:String				-> body of the notification
	badge:Int (optional)	-> badge of the notification
"""
def send_notification_basic(user,title,body,badge=0):

	send_notification_ios(user,title,body,badge)
	send_notification_android(user,title,body)



# !SECTION


#Public Function: Send notification to iOS Devices with data
"""
	user:String 			-> corresponding to receiver (Link to User)
	title:String 			-> title of the notification
	body:String				-> body of the notification
	data:JsonObject			-> data of the notification
	badge:Int (optional)	-> badge of the notification
"""
def send_notification_data_ios(user,title,body,data,badge=0,action=""):

	s = get_request_session()
	auth_key = get_auth_key()

	if auth_key == "":
		frappe.throw("Server key has been not set")
	else:
		frappe_userid = _get_topic(user)

		if frappe_userid != "":
			from random import randint
			id = str(randint(100000000, 999999999)) 
			# id = frappe.utils.now().split(' ')[1].replace(':', '').replace('.', '') 
			
			header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
			topic = "/topics/{}_ios".format(frappe_userid)
			content = {
				"to":topic,
				"notification":{
					"body":body,
					"title":title,
					# "badge":badge,
					"mutable_content":True,
					"sound": "default",
					"id" : id
				},
				"priority": "high"
			}
			if data:
				content["notification"].update(data)
			if action:
				content['notification'].update({"action":action})
			res = s.post(url=url,headers=header,data=json.dumps(content))

			#logging
			response_code = res.status_code
			if response_code == 200:
				res_json = res.json()
				message_id = res_json["message_id"]
				log_notification_success(response_code,message_id,user,topic,title,body,json.dumps(content),json.dumps(data),badge,id=id)
				# frappe.msgprint("iOS Success notified")
			else:
				error = res.text
				log_notification_failed(response_code,user,topic,title,body,error,id=id)
				frappe.throw(error)
		else:
			frappe.throw("User not found")

def send_notification_badge(user,badge):

	s = get_request_session()
	auth_key = get_auth_key()

	if auth_key == "":
		frappe.throw("Server key has been not set")
	else:
		frappe_userid = _get_topic(user)

		if frappe_userid != "":
			from random import randint
			id = str(randint(100000000, 999999999)) 
			# id = frappe.utils.now().split(' ')[1].replace(':', '').replace('.', '') 
			
			header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
			topic = "/topics/{}_ios".format(frappe_userid)
			content = {
				"to":topic,
				"notification":{
					# "badge":badge,
					"id" : id
				},
				"priority": "high"
			}
			res = s.post(url=url,headers=header,data=json.dumps(content))

			#logging
			response_code = res.status_code
			if response_code == 200:
				res_json = res.json()
				message_id = res_json["message_id"]
				log_notification_success(response_code,message_id,user,topic,"","",json.dumps(content),"",badge,id=id)
				# frappe.msgprint("iOS Success notified")
			else:
				error = res.text
				log_notification_failed(response_code,user,topic,"","",error,id=id)
				frappe.throw(error)
		else:
			frappe.throw("User not found")


#Public Function: Send notification to Android Devices with data
"""
	user:String 			-> corresponding to receiver (Link to User)
	title:String 			-> title of the notification
	body:String				-> body of the notification
	data:JsonObject			-> data of the notification
"""
def send_notification_data_android(user,title,body,data,action=""):

	s = get_request_session()
	auth_key = get_auth_key()

	if auth_key == "":
		frappe.throw("Server key has been not set")
	else:
		frappe_userid = _get_topic(user)

		if frappe_userid != "": 
			from random import randint
			id = str(randint(100000000, 999999999)) 
			# id = frappe.utils.now().split(' ')[1].replace(':', '').replace('.', '')

			header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
			topic = "/topics/{}_android".format(frappe_userid)
			content = {
				"to":topic,
				"data":{
					"action" : "GLOBAL",
					"body":body,
					"title":title,
					"id" : id
				}
			}
			content['data'].update(data)
			if action:
				content['data'].update({"action":action})
			print(content)
			res = s.post(url=url,headers=header,data=json.dumps(content))

			#logging
			response_code = res.status_code
			print(str(response_code))
			if response_code == 200:
				res_json = res.json()
				message_id = res_json["message_id"]
				log_notification_success(response_code,message_id,user,topic,title,body,json.dumps(content),json.dumps(data),id=id)
				# frappe.msgprint("Android Success notified")
			else:
				error = res.text
				log_notification_failed(response_code,user,topic,title,body,error,id=id)
				frappe.throw(error)
		else:
			frappe.throw("User not found")


#Public Function: Send notification to iOS and Android Devices with data
"""
	user:String 			-> corresponding to receiver (Link to User)
	title:String 			-> title of the notification
	body:String				-> body of the notification
	data:String				-> data of the notification
	badge:Int (optional)	-> badge of the notification
"""
def send_notification_data(user,title,body,data={},badge=0,action = ""):

	#check data json format
	try:
		if data:
			try:
				data_json = json.loads(data)
			except:
				data_json = data
		else:
			data_json = data
	except: 
		frappe.throw(error_result())

	if data_json:
		send_notification_data_ios(user,title,body,data_json,badge,action =action)
		send_notification_data_android(user,title,body,data_json, action =action)
	else:
		send_notification_ios(user,title,body,badge,action=action)
		send_notification_android(user,title,body,action = action)


# SECTION Global

#Public Function: Send notification to iOS and Android Devices
"""
	user:String 			-> corresponding to receiver (Link to User)
	title:String 			-> title of the notification
	body:String				-> body of the notification
	data:JsonObject			-> data of the notification
	badge:Int (optional)	-> badge of the notification
"""
def send_notification_global_image(title,body,data,badge=0,topics="",action=""):
	
	if not topics:
		android_topic = "/topics/ALL_ANDROID"
		ios_topic = "/topics/ALL_IOS"
	if topics == "vendor":
		android_topic = "/topics/ALL_VENDOR"
		android_topic = "/topics/ALL_VENDOR"
	
	send_notification_global_image_ios(title,body,data,ios_topic,action=action)
	send_notification_global_image_android(title,body,data,android_topic, action =action)

# Public Function Global
def send_notification_global_image_android(title,body,data,topic, action = ""):
	s = get_request_session()
	auth_key = get_auth_key()

	if auth_key == "":
		frappe.throw("Server key has been not set")
	else:
		from random import randint
		id = str(randint(100000000, 999999999)) 
		# id = frappe.utils.now().split(' ')[1].replace(':', '').replace('.', '')

		header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
		content = {
			"to":topic,
			"data":{
				"action" : "GLOBAL",
				"body":body,
				"title":title,
				"id" : id
			}
		}
		if data:
			content['data'].update(data)
		
		if action:
			content['data'].update({"action" : action})
		print(content)
		res = s.post(url=url,headers=header,data=json.dumps(content))

		#logging
		response_code = res.status_code
		print(str(response_code))
		if response_code == 200:
			res_json = res.json()
			message_id = res_json["message_id"]
			user = None
			log_notification_success(response_code,message_id,user,topic,title,body,json.dumps(content),json.dumps(data),id=id)
			# frappe.msgprint("Android Success notified")
		else:
			error = res.text
			user = None
			log_notification_failed(response_code,user,topic,title,body,error,id=id)
			frappe.throw(error)
		

def send_notification_global_image_ios(title,body,data,topic,badge=0,action=""):
	
	s = get_request_session()
	auth_key = get_auth_key()

	if auth_key == "":
		frappe.throw("Server key has been not set")
	else:
		from random import randint
		id = str(randint(100000000, 999999999)) 
		# id = frappe.utils.now().split(' ')[1].replace(':', '').replace('.', '')

		header = {"Authorization": "key={}".format(auth_key),"Content-Type": "application/json"}
		print(auth_key)
		content = {
			"to":topic,
			"notification":{
				"body":body,
				"title":title,
				"mutable_content":True,
				"sound": "default",
				"id" : id
			},
			"priority": "high"
		}
		if data:
			content['notification'].update(data)
		if action:
			content['notification'].update({"action":action})
		print(content)
		res = s.post(url=url,headers=header,data=json.dumps(content))

		#logging
		response_code = res.status_code
		if response_code == 200:
			res_json = res.json()
			message_id = res_json["message_id"]
			user = None
			log_notification_success(response_code,message_id,user,topic,title,body,json.dumps(content),json.dumps(data),badge,id=id)
			# frappe.msgprint("iOS Success notified")
		else:
			error = res.text
			user = None
			log_notification_failed(response_code,user,topic,title,body,error,id=id)
			frappe.throw(error)
		
# !SECTION

# ============================= FLUTTER SECTION =============================

def flutter_send_notification_data(user, title, body, image, data={}, badge=0):
	flutter_send_notification_data_android_ios(user=user, title=title, body=body, image=image ,data=data, badge=badge)
	
def flutter_send_notification_data_all(title, body, image, data={}, badge=0):
	flutter_send_notification_data_android_ios_all(user="Administrator", title=title, body=body, image=image, data=data, badge=badge)

def flutter_send_notification_data_android_ios(user, title, body, image="", data={}, badge=0):
	s = get_request_session()
	auth_key = get_auth_key()

	if auth_key == "" or not auth_key:
		frappe.throw("Server key has been not set")
	else:
		frappe_userid = _get_topic(user)

		if frappe_userid != "" or frappe_userid:
			from random import randint
			id = str(randint(100000000, 999999999))

			header = {
				"Authorization": "key={}".format(auth_key),
				"Content-Type": "application/json"
			}
			topic = "/topics/{}".format(frappe_userid)
			content = {
				"to": topic,
				"priority": "high",
				"notification": {
					"title": title,
					"body": body
				},
				"data":{
					"id" : id
				}
			}
			if image:
				content["notification"]["image"] = image

			if data:
				# data = json.loads(data)
				content['data'].update(data)
			
			res = s.post(url=url,headers=header,data=json.dumps(content))

			#logging
			response_code = res.status_code
			if response_code == 200:
				res_json = res.json()
				log_notification_success(response_code=response_code, message_id=res_json["message_id"], user=user, topic=topic, title=title, body=body, content=json.dumps(content), data=json.dumps(data), badge=badge, id=id)
			else:
				error = res.text
				log_notification_failed(response_code=response_code, user=user, topic=topic, title=title, body=body, error=error, id=id)
				frappe.throw(error)
		else:
			frappe.throw("User not found")

def flutter_send_notification_data_android_ios_all(user, title, body, image="", data={}, badge=0):
	s = get_request_session()
	auth_key = get_auth_key()

	if auth_key == "" or not auth_key:
		frappe.throw("Server key has been not set")
	else:
		from random import randint
		id = str(randint(100000000, 999999999))

		header = {
			"Authorization": "key={}".format(auth_key),
			"Content-Type": "application/json"
		}
		topic = "/topics/ALL"
		content = {
			"to": topic,
			"priority": "high",
			"notification": {
				"title": title,
				"body": body,
			},
			"data":{
				"id" : id
			}
		}
		if image:
			content["notification"]["image"] = image

		if data:
			# data = json.loads(data)
			content['data'].update(data)
		
		res = s.post(url=url,headers=header,data=json.dumps(content))

		#logging
		response_code = res.status_code
		if response_code == 200:
			res_json = res.json()
			log_notification_success(response_code=response_code, message_id=res_json["message_id"], user=user, topic=topic, title=title, body=body, content=json.dumps(content), data=json.dumps(data), badge=badge, id=id)
		else:
			error = res.text
			log_notification_failed(response_code=response_code, user=user, topic=topic, title=title, body=body, error=error, id=id)
			frappe.throw(error)