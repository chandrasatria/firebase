# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
 
from firebase.controller.user_notification_controller import UserNotificationController

class UserNotificationInbox(UserNotificationController):
	def before_insert(self):
		self.generate_date_and_time_inbox()
		

	def on_trash(self):
		self.delete_related_inbox_read()


	# End of hooks ----- 

	def generate_date_and_time_inbox(self):
		now = frappe.utils.now()
		date,time = self.generate_date_and_time()

		if not self.date_publish:
			self.date_publish = date
		if not self.time_publish:
			self.time_publish = time

