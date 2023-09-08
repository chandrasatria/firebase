import frappe

from firebase.firebase.error import error_result

def log_notification_success(response_code,message_id,user,topic,title,body,content,data="",badge=0,id=""):
	try:
		log_doc = frappe.new_doc("Firebase Log")
		log_doc.response_code = response_code
		log_doc.message_id = message_id
		log_doc.user = user
		log_doc.topic = topic
		log_doc.title = title
		log_doc.body = body
		log_doc.content = content
		log_doc.data = data
		log_doc.badge = badge
		log_doc.id = id

		log_doc.insert(ignore_permissions=True)
		frappe.db.commit()
	except:
		print("TODO: must be write on file log")


def log_notification_failed(response_code,user,topic,title,body,error,id=""):
	try:
		log_doc = frappe.new_doc("Firebase Log")
		log_doc.response_code = response_code
		log_doc.user = user
		log_doc.topic = topic
		log_doc.title = title
		log_doc.body = body
		log_doc.error = error
		log_doc.id = id

		log_doc.insert(ignore_permissions=True)
		frappe.db.commit()
	except:
		print("TODO: must be write on file log")