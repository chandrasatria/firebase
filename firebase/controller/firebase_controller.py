# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from firebase.controller.data_controller import DataController

class FirebaseController(DataController):
	def validate_condition(self, document_type, condition, throwback=False):
		"""
		Mengecek field condition = dict()
		"""
		temp_doc = frappe.new_doc(document_type)
		if condition and condition != "":
			try:
				frappe.safe_eval(condition, None, get_context(temp_doc.as_dict()))
			except Exception as e:
				self.error(message=_("The Condition '{0}' is invalid").format(condition), title="Error: Validate Condition", traceback=frappe.get_traceback(), throwback=throwback)
		else:
			return

	def send_notification_single_user(self, title, subtitle, detail, user):
		"""
		membuat user notification send message dan submit
		"""
		try:
			send_message = frappe.get_doc({
				"doctype"				: "User Notification Send Message",
				"repeat_notification"	: "Now",
				"title"					: title,
				"subtitle"				: subtitle,
				"using_notification"	: True,
				"using_inbox"			: True,
				"detail"				: detail,
				"destination"			: "Multiple"
				})
			send_message.append("user_notification_multiple_user_child", {
				"user"	: user
				})
			send_message.save()
			send_message.submit()
		except Exception as e:
			self.error(message=e, title="Error: Send Notification", traceback=frappe.get_traceback(), throwback=False)