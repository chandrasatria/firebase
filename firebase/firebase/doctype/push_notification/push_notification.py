# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from firebase.controller.firebase_controller import FirebaseController

class PushNotification(FirebaseController):
	def validate(self):
		self.validate_condition(document_type=self.document_type, condition=self.condition, throwback=True)
		self.validate_dictionary(dictionary=self.data, throwback=True)
		self.validate_jinja(string=self.subject, throwback=True)
		self.validate_jinja(string=self.message, throwback=True)

@frappe.whitelist()
def meta_fields(doctype):
	result = []
	meta_email = ""
	meta_email_fields = frappe.db.sql("""
		SELECT
			name,
			fieldname
		FROM `tabDocField`
		WHERE
			parent = %(doctype)s
			AND parenttype = "DocType"
			AND parentfield = "fields"
			AND ((
				fieldtype = "Link"
				AND options = "User"
			)OR(
				fieldtype = "Data"
				AND options = "Email"
			))
		""", {
		"doctype"	: doctype
		}, as_dict=True)
	if len(meta_email_fields) > 0:
		for mef in meta_email_fields:
			meta_email += "\n{fieldname}".format(fieldname = mef['fieldname'])
	result.append(meta_email)

	meta_doc = ""
	meta_doc_fields = frappe.db.sql("""
		SELECT
			name,
			fieldname
		FROM `tabDocField`
		WHERE
			parent = %(doctype)s
			AND parenttype = "DocType"
			AND parentfield = "fields"
			AND fieldtype NOT IN %(fieldtype)s
		""", {
		"doctype"	: doctype,
		"fieldtype" : ["Column Break", "Section Break"]
		}, as_dict=True)
	if len(meta_doc_fields) > 0:
		for mdf in meta_doc_fields:
			meta_doc += "\n{fieldname}".format(fieldname = mdf['fieldname'])	
	result.append(meta_doc)
	return result

def send_after_insert(doc, method):
	push_notifications = frappe.get_all("Push Notification", fields="name", filters=[['send_alert_on', '=', 'New'], ['document_type', '=', doc.doctype]])
	if len(push_notifications) > 0:
		frappe.enqueue('firebase.firebase.doctype.push_notification.push_notification.send_notification', push_notifications=push_notifications, doc=doc)
		# send_notification(push_notifications=push_notifications, doc=doc)
	else:
		pass

def send_validate(doc, method):
	push_notifications = frappe.get_all("Push Notification", fields="name", filters=[['send_alert_on', 'in', ['Save', 'Value Change']], ['document_type', '=', doc.doctype]])
	if len(push_notifications) > 0:
		frappe.enqueue('firebase.firebase.doctype.push_notification.push_notification.send_notification', push_notifications=push_notifications, doc=doc)
		# send_notification(push_notifications=push_notifications, doc=doc)
	else:
		pass

def send_on_submit(doc, method):
	push_notifications = frappe.get_all("Push Notification", fields="name", filters=[['send_alert_on', '=', 'Submit'], ['document_type', '=', doc.doctype]])
	if len(push_notifications) > 0:
		frappe.enqueue('firebase.firebase.doctype.push_notification.push_notification.send_notification', push_notifications=push_notifications, doc=doc)
		# send_notification(push_notifications=push_notifications, doc=doc)
	else:
		pass

def send_notification(push_notifications, doc):
	try:
		for pns in push_notifications:
			push_notification = frappe.get_doc("Push Notification", pns['name'])
			if check_value_change(push_notification=push_notification, doc=doc) and check_condition(push_notification=push_notification, doc=doc):
				if len(push_notification.recipients) > 0:
					for r in push_notification.recipients:
						user = getattr(doc, r.receiver_by_document_field, None)
						if user != None and user != "":
							send(push_notification=push_notification, user=user, doc=doc)
						else:
							pass
				else:
					pass
			else:
				pass
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), _("ERROR: Push Notification Send Notification"))
	frappe.db.commit()

def get_context(doc):
	from frappe.utils import nowdate
	from frappe.utils.safe_exec import get_safe_globals
	return {
		"doc" 		: doc, 
		"nowdate"	: nowdate(),
		"frappe"	: frappe._dict(utils=get_safe_globals().get("frappe").get("utils"))
		}

def check_condition(push_notification, doc):
	if push_notification.condition and not frappe.safe_eval(push_notification.condition, None, get_context(doc)):
		return False
	else:
		return True
	
def check_value_change(push_notification, doc):
	if push_notification.send_alert_on == "Value Change" and push_notification.value_changed:
		db_doc = frappe.db.sql("""
			SELECT {field}
			FROM `tab{doctype}`
			WHERE name = %(name)s
			""".format(field=push_notification.value_changed, doctype=doc.doctype), {
			"name" : doc.name
			}, as_dict=True)
		if len(db_doc) > 0:
			if db_doc[0].get(push_notification.value_changed, None) != getattr(doc, push_notification.value_changed, None):
				return True
			else:
				return False
		else:
			return False
	else:
		return True

def send(push_notification, user, doc):
	context = get_context(doc)
	context = {"doc": doc, "alert": push_notification, "comments": None}
	subject = push_notification.subject
	if "{" in subject:
		subject = frappe.render_template(push_notification.subject, context)
	message = frappe.render_template(push_notification.message, context)

	if push_notification.channel == "Firebase":
		if push_notification.firebase_method == "Basic":
			from firebase.firebase.notification import send_notification_basic
			send_notification_basic(user=user, title=subject, body=message, badge=0)
		
		elif push_notification.firebase_method == "Basic Data":
			from firebase.firebase.notification import send_notification_data
			send_notification_data(user=user, title=subject, body=message, data=push_notification.data, badge=0, action="")
		
		elif push_notification.firebase_method == "Global Image":
			from firebase.firebase.notification import send_notification_global_image
			send_notification_global_image(title=subject, body=message, data=push_notification.data, badge=0, topics=None, action="")
		
		elif push_notification.firebase_method == "Flutter Data":
			from firebase.firebase.notification import flutter_send_notification_data
			flutter_send_notification_data(user=user, title=subject, body=message, data=push_notification.data, badge=0)

		elif push_notification.firebase_method == "Flutter Data Global":
			from firebase.firebase.notification import flutter_send_notification_data_all
			flutter_send_notification_data_all(title=subject, body=message, data=push_notification.data, badge=0)

		else:
			pass
	else:
		pass