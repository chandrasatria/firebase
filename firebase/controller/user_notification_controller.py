import frappe

from firebase.controller.data_controller import DataController
from frappe import _

from frappe.realtime import publish_progress

class UserNotificationController(DataController):
    def generate_date_and_time(self):
        now = frappe.utils.now()
        date = now[:10]
        time = frappe.utils.get_time(now[11:19])
        return date,time

    # Notification Inbox
    def delete_related_inbox_read(self):
        if self.name:
            idx_progress = 1
            fga_inbox_read = frappe.get_all("User Notification Inbox Read",filters=[["user_notification_inbox","=",self.name]],fields="name")
            for item in fga_inbox_read:
                idx_progress += 1   
                if item["name"]:
                    del_doc = frappe.delete_doc("User Notification Inbox Read", item["name"])
                percent = (idx_progress/len(fga_inbox_read)) * 100
                publish_progress(percent=percent, title=_("Deleting User Notification Inbox Read"), doctype=self.doctype, docname=self.name, description=item["name"])
        frappe.db.commit()

    # Send Message
    def delete_inbox(self):
        if self.name:
            idx_progress = 1
            fga_inbox = frappe.get_all("User Notification Inbox",filters=[["user_notification_send_message","=",self.name]],fields="name")
            for item in fga_inbox:
                idx_progress += 1   
                if item["name"]:
                    del_doc = frappe.delete_doc("User Notification Inbox", item["name"])
                percent = (idx_progress/len(fga_inbox)) * 100
                publish_progress(percent=percent, title=_("Deleting User Notification Inbox"), doctype=self.doctype, docname=self.name, description=item["name"])
        frappe.db.commit()


