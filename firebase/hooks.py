# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "firebase"
app_title = "Firebase"
app_publisher = "DAS"
app_description = "App to manage Google Firebase"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "digitalasiasolusindo.developer@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/firebase/css/firebase.css"
# app_include_js = "/assets/firebase/js/firebase.js"

# include js, css files in header of web template
# web_include_css = "/assets/firebase/css/firebase.css"
# web_include_js = "/assets/firebase/js/firebase.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "firebase.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "firebase.install.before_install"
# after_install = "firebase.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "firebase.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"*": {
		"after_insert"	: ["firebase.firebase.doctype.push_notification.push_notification.send_after_insert"],
		"validate"		: ["firebase.firebase.doctype.push_notification.push_notification.send_validate"],
		"on_submit"		: ["firebase.firebase.doctype.push_notification.push_notification.send_on_submit"]
	}
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "cron": {
		"0 * * * *":[
			# NOTE untuk send user notification
			"firebase.user_notification.schedule.user_notification_send_message_scheduler"
		],
		"30 * * * *":[
			# NOTE untuk send user notification
			"firebase.user_notification.schedule.user_notification_send_message_scheduler"
		]
    },
}

# Testing
# -------

# before_tests = "firebase.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "firebase.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "firebase.task.get_dashboard_data"
# }

