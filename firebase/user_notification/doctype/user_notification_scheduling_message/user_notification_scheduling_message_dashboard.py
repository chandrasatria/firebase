from frappe import _

def get_data():
	return {
		'fieldname': 'user_notification_scheduling_message',
		'transactions': [
			{
				'label': _('User Notification Send Message'),
				'items': ['User Notification Send Message']
			}
		]
	}