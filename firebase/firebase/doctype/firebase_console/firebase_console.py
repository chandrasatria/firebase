# -*- coding: utf-8 -*-
# Copyright (c) 2019, digitalasiasolusindo@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from firebase.firebase.notification import send_notification_basic, send_notification_data, flutter_send_notification_data

class FirebaseConsole(Document):
	def user_topic_send_notification(self):
		flutter_send_notification_data(user=self.user, title=self.title, body=self.body, data=self.data, badge=self.badge, image=self.image)
		
		# if self.is_using_data == 0:
		# 	send_notification_basic(self.user,self.title,self.body,self.badge)
		# else:
		# 	send_notification_data(self.user,self.title,self.body,self.data,self.badge)