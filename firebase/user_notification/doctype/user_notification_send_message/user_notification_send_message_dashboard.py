from frappe import _

def get_data():
	return {
		'fieldname': 'user_notification_send_message',
		'transactions': [
			{
				'label': _('User Notification Inbox'),
				'items': ['User Notification Inbox']
			}
		]
	}