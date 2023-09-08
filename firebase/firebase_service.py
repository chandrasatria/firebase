from oauth2client.service_account import ServiceAccountCredentials
from frappe.utils import get_request_session
import json

PROJECT_ID = "prospective-dev"

def get_access_token():
	SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
	SERVICE_ACCOUNT_FILE = '/home/frappe/frappe-bench/apps/firebase/firebase/service.json'

	credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
	access_token_info = credentials.get_access_token()
	return access_token_info.access_token


def send_notif(title, subtitle):
	s = get_request_session()
	payload = {
	  "message": {
	    "topic": "ALL_IOS",
	    "notification": {
	      "title": title,
	      "body": subtitle
	    },
	    "data": {
	      "id": "1"
	    },
	    "android": {
	      "notification": {
	        "click_action": "TOP_STORY_ACTIVITY",
	        "body": subtitle
	      }
	    },
	    "apns": {
	      "payload": {
	        "aps": {
	          "category" : "NEW_MESSAGE_CATEGORY",
	          "content-available": 1
	        }
	      }
	    }
	  }
	}
	header = {"Authorization": "Bearer " + get_access_token(), 'Content-Type': 'application/json; UTF-8'}
	url = "https://fcm.googleapis.com/v1/projects/{}/messages:send".format(PROJECT_ID)
	res = s.post(url=url,headers=header,data=json.dumps(payload))
	print(res)
	return res