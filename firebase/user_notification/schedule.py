
import frappe
from firebase.user_notification.helper import strToDate

# Untuk kirim notification secara otomatis dalam kurun waktu 30 menit an
def user_notification_send_message_scheduler():
	from firebase.user_notification.helper import log_cronjob
	log_cronjob("firebase.user_notification.schedule.user_notification_send_message_scheduler")
	today = frappe.utils.now()
	waktu = today[11:][:5]
	time_class = waktu[:2]+":"+"00" if int(waktu[3:]) < 30 else waktu[:2]+":"+"30"
	print(time_class)
	print(strToDate(today))
	print(time_class)
	fga = frappe.get_all("User Notification Send Message", fields = "*", filters=[["date_publish","=", strToDate(today)],["time_publish","=",time_class],["repeat_notification","=","Once"]])
	print(fga)	
	for item in fga:
		doc = frappe.get_doc("User Notification Send Message",item["name"])
		from firebase.user_notification.doctype.user_notification_send_message.user_notification_send_message import send_to_inbox, user_notification_send_notification
		if item["using_inbox"] == 1:
			send_to_inbox(doc)
		if item["using_notification"] == 1:
			user_notification_send_notification(doc)
		doc.docstatus = 1
		doc.status = "Sent"
		doc.save(ignore_permissions=True)
		doc.submit()
		frappe.db.commit()
			