# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from frappe.model.document import Document

class HandlingController(Document):
	def error(self, message=None, title=None, traceback=None, throwback=False):
		"""
		Mencetak di Error Log dan prompt ke user jika dibutuhkan
		"""
		# compile message and title di error log
		log_message = "TRACEBACK:\n{traceback}\nMESSAGE:\n{message}\nDOCUMENT:\n{document}".format(traceback=traceback, message=message, document=self.as_dict(convert_dates_to_str=True))
		log_title = title
		# membuat error log
		frappe.log_error(log_message, log_title)

		# prompt ke user
		if throwback:
			frappe.msgprint(msg=message, title=_("Something went wrong"), raise_exception=throwback, as_table=False, as_list=False, indicator=None, alert=False, primary_action=None, is_minimizable=None, wide=None)
		else:
			return