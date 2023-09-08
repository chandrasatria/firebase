// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('User Notification Scheduling Message', {
	set_arknet_user_query: function(frm) {
		cur_frm.set_query("arknet_user", "user_notification_multiple_user_child", function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
					"filters": [
						['Arknet User', 'workflow_state', 'NOT IN', ["Blocked", "Cancelled"]]
					]

			}
		})
	},
	onload: function (frm) {
		frm.events.set_arknet_user_query(frm)
	},
	refresh: function (frm) {
		frm.events.hide_read_only_only(["monthly_type", "date", "last_date", "week_of", "day"], 0)
		frm.events.change_view_schedule_repetition(cur_frm)
	},


	// STUB Function
	change_view_schedule_repetition: function (frm) {
		if (frm.doc.schedule_repetition == "Weekly") {
			frm.events.hide_read_only_reqd_only(["day"], 1)
			frm.events.hide_read_only_reqd_only(["monthly_type", "date", "last_date", "week_of", "last_week"], 0)
		} else if (frm.doc.schedule_repetition == "Monthly") {
			frm.events.hide_read_only_reqd_only(["monthly_type"], 1)
			frm.events.hide_read_only_reqd_only(["day"], 0)
			if (frm.doc.monthly_type == "Date") {
				if (frm.doc.last_date == 1) {
					frm.events.hide_read_only_reqd_only(["date", "day", "week_of", "last_week"], 0)
					frm.events.hide_read_only_reqd_only(["monthly_type", "last_date"], 1)
				} else {
					frm.events.hide_read_only_only(["last_date"], 0)
					frm.events.hide_read_only_reqd_only(["monthly_type", "date"], 1)
					frm.events.hide_read_only_reqd_only(["week_of", "last_week"], 0)
				}
			} else if (frm.doc.monthly_type == "Week Of") {
				if (frm.doc.last_week == 1) {
					frm.events.hide_read_only_reqd_only(["day", "date", "last_date", "week_of"], 0)
					frm.events.hide_read_only_reqd_only(["monthly_type", "last_week", "day"], 1)
				} else {
					frm.events.hide_read_only_reqd_only(["day", "date", "last_date"], 0)
					frm.events.hide_read_only_reqd_only(["monthly_type", "week_of", "day", "last_week"], 1)
				}
			} else {
				// frm.set_df_property("monthyly_type","reqd",1)
			}
		}
	},

	hide_read_only_only: function (list, stat) {
		$.each(list, function (i, l) {
			cur_frm.set_df_property(l, "reqd", 0)
			cur_frm.set_df_property(l, "hidden", stat)
			cur_frm.set_df_property(l, "read_only", stat)
		})
	},

	hide_read_only_reqd_only: function (list, stat) {

		$.each(list, function (i, l) {
			const lawan_stat = stat == 0 ? 1 : 0;

			cur_frm.set_df_property(l, "reqd", stat)
			cur_frm.set_df_property(l, "hidden", lawan_stat)
			cur_frm.set_df_property(l, "read_only", lawan_stat)
		})
	},
	schedule_repetition: function (frm) {
		frm.events.change_view_schedule_repetition(frm)
	},
	monthly_type: function (frm) {
		frm.events.change_view_schedule_repetition(frm)
	},
	last_week: function (frm) {
		frm.events.change_view_schedule_repetition(frm)
	},
	last_date: function (frm) {
		frm.events.change_view_schedule_repetition(frm)
	},



});