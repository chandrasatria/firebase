# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from firebase.controller.handling_controller import HandlingController

class DataController(HandlingController):
	def validate_jinja(self, string, throwback=False):
		"""
		Mengecek field Jinja
		reference: from frappe.utils.jinja import validate_template
		"""
		if string is not None and string != "":
			import frappe
			from jinja2 import TemplateSyntaxError

			from frappe.utils.jinja import get_jenv
			jenv = get_jenv()
			try:
				jenv.from_string(string)
			except TemplateSyntaxError as e:
				self.error(message='Line {}: {}'.format(e.lineno, e.message), title="Error: Validate Jinja", traceback=frappe.get_traceback(), throwback=throwback)
		else:
			return

	def validate_dictionary(self, dictionary, throwback=False):
		"""
		Mengecek field Dictionary
		"""
		if dictionary is not None and dictionary != "":
			state = False
			try:
				from ast import literal_eval
				# convert dari string ke dictionary
				data = literal_eval(dictionary)
				# cek dictionary
				if isinstance(data, dict):
					state = True
				else:
					state = False
			except:
				# jika gagal saat convert, berarti bukan dictionary
				state = False
			
			if state == False:
				self.error(message=_("The Data '{0}' is invalid").format(dictionary), title="Error: Validate Dictionary", traceback=frappe.get_traceback(), throwback=throwback)
			else:
				pass
		else:
			return