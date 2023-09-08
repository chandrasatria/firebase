// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Push Notification', {
	refresh: function(frm) {
		frm.events.document_type(frm);
		frm.events.send_alert_on(frm);
	},

	document_type: function(frm) {
		if (frm.doc.document_type) {
			frappe.call({
				method: "firebase.firebase.doctype.push_notification.push_notification.meta_fields",
				args: {
					'doctype': frm.doc.document_type
				},
				callback: function(data){
					var df = frappe.meta.get_docfield("Push Notification Recipient", "receiver_by_document_field", frm.doc.name);
					df.options = data.message[0];

					frm.set_df_property("value_changed", "options", data.message[1]);
					frm.refresh_fields();
				}
			});
		}
		frm.refresh_fields();
	},

	send_alert_on: function(frm) {
		if (frm.doc.send_alert_on == "Value Change") {
			frm.set_df_property("value_changed", "reqd", 1);
		}else{
			frm.set_df_property("value_changed", "reqd", 0);
		}
	}
});
