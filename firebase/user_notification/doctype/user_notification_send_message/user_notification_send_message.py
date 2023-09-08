# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

from firebase.user_notification.setting import get_un_variabel, image_using_complete_url
from frappe.utils.background_jobs import enqueue 

from frappe.utils import get_url
from firebase.user_notification.helper import check_and_append_url_image

from firebase.controller.user_notification_controller import UserNotificationController

try:
	from firebase.firebase.notification import get_auth_key
except:
	frappe.throw(_("Cannot find")+ " firebase.notification " + (_("Please contact Administrator.")))


class UserNotificationSendMessage(UserNotificationController):
	def validate(self):
		self.validate_general_settings()
		self.validate_rule_send_message()

	def on_update(self):
		if self.docstatus == 1:
			if self.repeat_notification == "Now":
				if self.name and self.status == "Not Sent":
					fga = frappe.get_all("User Notification Inbox", fields="name", filters=[["user_notification_send_message", "=", self.name]])
					if len(fga) == 0:
						if self.using_notification:
							user_notification_send_notification(self)
						if self.using_inbox:
							send_to_inbox(self)
						frappe.db.sql("UPDATE `tabUser Notification Send Message` SET status = 'Sent' WHERE name = '{}'".format(self.name))
						frappe.db.commit()
						self.reload()

			if self.using_inbox and self.status != "Sent":
				pass

	def on_trash(self):
		self.delete_inbox()

	# End of hooks

	
	def validate_general_settings(self):
		# Check server key
		url_firebase_setting = frappe.utils.get_url()+"/desk#Form/Firebase Setting/Firebase Setting"
		if not get_auth_key():
			frappe.throw(_("Server Key must be set, please setup here")+" <a href = '"+url_firebase_setting+"'>"+ str(" "+url_firebase_setting) + "</a>")
		doc_un_settings = frappe.get_single("User Notification Settings")
		if doc_un_settings:
			check = False
			if doc_un_settings.get("send_to_android") == 1:
				check =True
			elif doc_un_settings.get("send_to_ios") == 1:
				check = True
			elif doc_un_settings.get("send_to_flutter") == 1:
				check = True
			elif doc_un_settings.get("send_to_web") == 1:
				check = True
			if check == False:
				frappe.throw(_("Notification must be set, please setup here")+" <a href = '/desk#Form/User%20Notification%20Settings'>"+ str(" Click me ") + "</a>")


	def validate_rule_send_message(self):
		if not self.using_inbox and not self.using_notification:
			frappe.throw(_("Please check Using Notification or/and Using Inbox"))


# Function local
# NOTE ini sangat dipake
def send_to_inbox(self):
	if self.destination == "Now":
		date_publish = frappe.utils.nowdate()
		time_publish = frappe.utils.get_time(str(frappe.utils.nowtime())[:8]),
	else:
		date_publish = self.date_publish
		time_publish = self.time_publish
	# time_pub = str(self.time_publish)+":00" if len(str(self.time_publish)) == 5 else self.time_publish
	doc_dict = {
		"doctype" : "User Notification Inbox",
		"destination" : self.destination,
		"user_notification_send_message" : self.name,
		"date_publish": date_publish,
		"time_publish" : time_publish,
		"title" : self.title,
		"detail" : self.detail,
		"image" : self.image,
		"icon" : self.icon
	}
	if self.destination == "Multiple":
		for item in self.user_notification_multiple_user_child:
			if not doc_dict.get("user_notification_inbox_user_child"):
				doc_dict["user_notification_inbox_user_child"] = []
			append_data = ({
				"user": item.get("user")
			})
			doc_dict["user_notification_inbox_user_child"].append(append_data)
			# if not doc.get("user_notification_inbox_user_child"):
			# 	doc.user_notification_inbox_user_child = []
			# print(get_un_variabel("customer"))
			# print(str(item.get(get_un_variabel("customer"))))
			# data_to_append = {get_un_variabel("customer"): item.get(get_un_variabel("customer"))}
			# print(str(data_to_append))
			# doc["user_notification_inbox_user_child"].append(data_to_append)
			# print(str(vars(doc_dict)))
	# frappe.msgprint(str(doc_dict))
	doc = frappe.get_doc(doc_dict)
	doc.save(ignore_permissions=True)
	frappe.db.commit()



def user_notification_send_notification(self):
	if self.destination == "Multiple":
		list_user = []
		for user in self.user_notification_multiple_user_child:
			if user.get("user"):
				list_user.append(user.get("user"))
		
		for index,user_social_login_item in enumerate(list_user,0):
			from firebase.firebase.notification import send_notification_data
			data_inbox = {"action":"NOTIFICATION"}
			if self.get("image"):
				image_url = check_and_append_url_image(url_image=self.get("image")) + self.get("image")
			else:
				image_url = ""
				
			# Badge TODO
			# from firebase.user_notification.api import get_unread_inbox_with_user
			# badge = get_unread_inbox_with_user(list_customer[index])
			process_enqueue(tipe="User", now=True, user =user_social_login_item, title=self.title, body=self.subtitle, data=data_inbox, image = image_url)

	if self.destination == "Global":
		from firebase.firebase.notification import send_notification_data
		data_inbox = {"action":"NOTIFICATION"}
		if self.get("image"):
			image_url = check_and_append_url_image(url_image=self.get("image")) + self.get("image")
		else:
			image_url = ""
		process_enqueue(tipe="Global",now=True, title=self.title, body=self.subtitle, data=data_inbox, image =image_url)
		

def process_enqueue(tipe = "", now = True, user= "",title="",body="",data="",badge="",image="",action="NOTIFICATION"):
	if not tipe:
		return
	if tipe =="Global":
		from firebase.firebase.notification import send_notification
		# send_notification(
		# 	platform="flutter",
		# 	target_notification="Global",
		# 	notification = {
		# 		"title" : title,
		# 		"body" : body,
		# 		"image" : image
		# 	},
		# 	data={"action" : action}
		# )
		# TODO when platform > 1 di User Notification Setting
		enqueue("firebase.firebase.notification.send_notification", platform="flutter",
			target_notification="Global",
			notification = {
				"title" : title,
				"body" : body,
				"image" : image
			},
			data={"action" : action})
	elif tipe == "User":
		from firebase.firebase.notification import send_notification
		send_notification(
			platform="flutter",
			target_notification="User",
			notification = {
				"title" : title,
				"body" : body,
				"image" : image
			},
			data={"action" : action},
			user = user
		)
		# enqueue("firebase.firebase.notification.send_notification", platform="flutter",
		# 	target_notification="User",
		# 	notification = {
		# 		"title" : title,
		# 		"body" : body,
		# 		"image" : image
		# 	},
		# 	data={"action" : action},
		# 	user = user)