# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe.utils import cint, getdate, formatdate, today

from firebase.user_notification.helper import strToDate
from firebase.user_notification.helper import getEveryDays_list,getMonthDate_list,getMonthWeek_list

class UserNotificationSchedulingMessage(Document):
	def before_save(self):
		if not self.get("schedule_date"):
			self.generate_date_function()

	def on_submit(self):
		if self.docstatus == 1:
			self.create_user_notification_send_message()

	# SUBSECTION BUTTON
	def generate_date(self):
		self.generate_date_function()
		
	# SUBSECTION function on_submit
	def create_user_notification_send_message(self):
		if self.docstatus == 1:
			for item in self.schedule_date:
				doc = frappe.get_doc({
					"user_notification_scheduling_message" : self.name,
					"status": "Not Sent",
					"repeat_notification": "Once",
					"date_publish": item.date,
					"time_publish": item.time,
					"title": item.title,
					"subtitle": item.subtitle,
					"using_notification": item.using_notification,
					"using_inbox": item.using_inbox,
					"detail": item.detail,
					"destination": self.destination,
					"doctype": "User Notification Send Message",
					"user_notification_multiple_user_child": self.user_notification_multiple_user_child
				})
				doc.save(ignore_permissions=True)
			frappe.db.commit()

	# SUBSECTION function before_save
	def generate_date_function(self):
		last_idx = max([cint(d.idx) for d in self.get("schedule_date")] or [0,])
		repeat_list = []
		if(self.schedule_repetition == "Every Day"):
			repeat_list = getEveryDays_list(self.from_date, self.to_date)
		elif(self.schedule_repetition == "Weekly"):
			repeat_list = get_weekly_off_date_list(self.from_date, self.to_date, self.day)
		elif(self.schedule_repetition == "Monthly"):
			if(self.monthly_type == "Date"):
				if(self.last_date ==1):
					repeat_list = getMonthDate_list(self.from_date, self.to_date, 31)
				else:
					repeat_list = getMonthDate_list(self.from_date, self.to_date, int(self.date))
			elif(self.monthly_type == "Week Of"):
				if(self.last_week == 1):
					repeat_list = getMonthWeek_list(self.from_date, self.to_date, -1 , self.day)
				else:
					repeat_list = getMonthWeek_list(self.from_date, self.to_date, self.week_of, self.day)

		
		list_date = [ str(d.date) for d in self.schedule_date ]
		list_child_schedule_date = [d.name for d in self.schedule_date]
		for i, d in enumerate(repeat_list):
			if str(d) not in list_date:
				# frappe.msgprint(str(d))
				schedule_date_self = self.append('schedule_date', {})
				schedule_date_self.date = d
				schedule_date_self.time = self.time
				schedule_date_self.idx = last_idx + i + 1
				
				# For adding in child table
				schedule_date_self.url = self.url
				schedule_date_self.title = self.title
				schedule_date_self.subtitle = self.subtitle
				schedule_date_self.using_notification = self.using_notification
				schedule_date_self.using_inbox = self.using_inbox
				schedule_date_self.detail = self.detail
			else:
				schedule_index = next((index for (index, d) in enumerate(self.schedule_date) if d.name == list_child_schedule_date[i]), None)
				self.schedule_date[schedule_index].update({
					"url" : self.url,
					"title" :self.title,
					"subtitle" :self.subtitle,
					"using_notification" : self.using_notification,
					"using_inbox" :self.using_inbox,
					"detail" :self.detail
				})
			

# INI WEEKLY
def get_weekly_off_date_list( start_date, end_date, day):
	start_date, end_date = getdate(start_date), getdate(end_date)

	from dateutil import relativedelta
	from datetime import timedelta
	import calendar
	date_list = []
	existing_date_list = []
	weekday = getattr(calendar, (day).upper())
	reference_date = start_date + relativedelta.relativedelta(weekday=weekday)

	existing_date_list = []

	while reference_date <= end_date:
		if reference_date not in existing_date_list:
			date_list.append(reference_date)
		reference_date += timedelta(days=7)
	
	return date_list