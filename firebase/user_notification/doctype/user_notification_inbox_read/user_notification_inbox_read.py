# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

from firebase.user_notification.setting import get_un_variabel

class UserNotificationInboxRead(Document):
	def before_insert(self):
		if self.user and self.user_notification_inbox:
			val = frappe.get_value("User Notification Inbox Read", {"user" : self.user , "user_notification_inbox" : self.user_notification_inbox})
			if val:
				frappe.throw(_("User Notification Inbox already inserted"))


	def after_insert(self):
		from firebase.firebase.notification import send_notification_badge
		from firebase.user_notification.api import get_unread_inbox_with_user
		
		badge = get_unread_inbox_with_user(self.user)
		user = frappe.get_value(get_un_variabel("Customer"),self.user,get_un_variabel("user"))
		# frappe.msgprint(str(user))
		send_notification_badge(user, badge)
