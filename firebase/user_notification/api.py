import frappe
from frappe import _
import datetime
import json
from firebase.user_notification.validation import success_format,error_format
import ast
import urllib.parse

from firebase.user_notification.setting import get_un_variabel

LIMIT_PAGE = 20

@frappe.whitelist(allow_guest=True)
def ping():
	return "pong"

@frappe.whitelist(allow_guest=True)
def post_ping_guest():
	post = json.loads(frappe.request.data)
	return str(post)

@frappe.whitelist(allow_guest=False)
def post_ping():
	post = json.loads(frappe.request.data)
	return str(post)

@frappe.whitelist(allow_guest=False)
def get_user_id_by_session():
	# return frappe.get_value(get_un_variabel("Customer"), {get_un_variabel("user"): frappe.session.user}, "name")
	return frappe.session.user

@frappe.whitelist(allow_guest=False)
def get_session():
	return frappe.session

# Get all Inbox
@frappe.whitelist()
def get_all_notification_on_user(user = ""):
	field_conn = user
	if user:
		custom_user = frappe.get_value(get_un_variabel("Customer"), {get_un_variabel("user"): user}, "name")
	else:
		custom_user = get_user_id_by_session()
	response = frappe.get_all("User Notification Inbox", filters=[["destination","=","Global"]], fields="name")
	return response

@frappe.whitelist(allow_guest=False)
def get_inbox(page=0,search = "%"):
	""" List Inbox """
	user = get_user_id_by_session()
	page = int(page)
	if search != "%":
		search = "%"+search+"%"
	# print(user)
	# return user
	# print()
	sql = frappe.db.sql(""" SELECT * FROM `tabUser Notification Inbox` WHERE (destination = "Global" OR (name IN (SELECT parent FROM `tabUser Notification Inbox User Child` WHERE user = %(user)s))) AND (title LIKE %(search)s OR detail LIKE  %(search)s) ORDER BY creation DESC, date_publish DESC, time_publish DESC LIMIT {LIMIT_PAGE} OFFSET {page}""".format(LIMIT_PAGE = LIMIT_PAGE, page = page),{
		"user" : user,
		"search" : search
	},as_dict=True)
	fgl = frappe.get_list("User Notification Inbox Read", fields="*", filters=[["user","=",user]])
	fgl_dict = {}
	for item in fgl:
		if item.get("user_notification_inbox",""):
			fgl_dict[item["user_notification_inbox"]] = item
	for item in sql:
		item["date_publish"] = item["date_publish"] if item["date_publish"] else "-"
		item["time_publish"] = item["time_publish"] if item["time_publish"] else "-"
		if fgl_dict.get(item["name"],""):
			item["read"] = 1
		else:
			item["read"] = 0

	return success_format(sql)


@frappe.whitelist(allow_guest=False)
def get_detail_inbox(inbox):
	""" Ambil Detail Inbox, lalu sistem menambahkan sudah dibaca """
	try:
		user = get_user_id_by_session()
		# q : ask mau pake user permission apa tidak
		# a : Kata ko dewe ngga usah, user perm buat yang di backend aja
		fga = frappe.get_list("User Notification Inbox", filters= [["User Notification Inbox","name","=",inbox]], fields="*")
		if len(fga) >0:
			if fga[0]["destination"] == "Multiple":
				sql = frappe.db.sql("""SELECT * FROM `tabUser Notification Inbox User Child` WHERE parent = %(parent)s AND user = %(user)s""",{
					"parent" : fga[0]["name"],
					"user" : user
				},as_dict=True)
				if len(sql) == 0:
					return error_format(_("Sorry, User not permitted to view this document."))
			create_inbox_read(inbox, user)
			return success_format([fga[0]])
		else:
			return success_format(_("Sorry, User not permitted to view this document."))
	except:
		return success_format(_("Sorry, Inbox not found."))


@frappe.whitelist(allow_guest=False)
def read_all_inbox():
	""" Digunakan untuk tandai semua sudah baca """
	
	user = get_user_id_by_session()
	sql = get_all_personal_inbox(get_un_variabel("customer"), user)
	try:
		for item in sql:
			print(item["parent"])
			create_inbox_read(item["parent"],user)
		
		sql_global = get_all_global_inbox()
		for item in sql_global:
			create_inbox_read(item["name"],user)
	except:
		pass

	return success_format(_("Successfully marked read"))
	

@frappe.whitelist(allow_guest=False)
def get_unread_inbox():
	try:
		user = get_user_id_by_session()
		count_unread = get_unread_inbox_with_user(user)
		if (count_unread.get("data")):
			return count_unread
		return success_format(count_unread)
	except:
		return success_format(_("Sorry, Inbox not found."))

@frappe.whitelist(allow_guest=False)
def get_unread_inbox_with_user(customer= ""):
	if not customer:
		customer = frappe.get_value(get_un_variabel("Customer"), {get_un_variabel("user"): frappe.session.user}, "name")
	sql = frappe.db.sql(""" SELECT * FROM `tabUser Notification Inbox` WHERE destination = 'Global' OR name IN (SELECT parent FROM `tabUser Notification Inbox User Child` WHERE {customer} = %(user)s ) ORDER BY date_publish DESC, time_publish DESC""".format(customer = get_un_variabel("customer")),{
		"user" : customer
	},as_dict=True)
	print(sql)
	fgl = frappe.get_all("User Notification Inbox Read", fields="*", filters=[[get_un_variabel("customer"),"=",customer]])
	fgl_dict = {}
	print(fgl)
	count_unread = 0

	for item in fgl:
		if item.get("user_notification_inbox",""):
			fgl_dict[item["user_notification_inbox"]] = item
	for item in sql:
		if fgl_dict.get(item["name"],""):
			item["read"] = 1
		else:
			count_unread += 1
	
	return success_format(count_unread)

def create_inbox_read(user_notification_inbox,customer):
	try:
		doc_inbox_read = frappe.get_doc({
			"user": customer,
			"user_notification_inbox": user_notification_inbox,
			"doctype" : "User Notification Inbox Read"
		})
		doc_inbox_read.save(ignore_permissions=True)
		frappe.db.commit()
		print("doc_inbox_read")
	except:
		
		print(frappe.get_traceback())
	



# STUB function

def get_all_personal_inbox(customer, user):
	print(customer)
	print(user)
	# Ini ngga pake %(customer)s karna ga jalan
	sql = frappe.db.sql("""SELECT * FROM `tabUser Notification Inbox User Child` WHERE {customer} = %(user)s """.format(customer= get_un_variabel("customer")),{ "user" : user},as_dict=True)
	print(sql)
	return sql

def get_all_global_inbox():
	sql_global = frappe.db.sql(""" SELECT name FROM `tabUser Notification Inbox` WHERE destination = 'Global' """,as_dict=True)
	return sql_global