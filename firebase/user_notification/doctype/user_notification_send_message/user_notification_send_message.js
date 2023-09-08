// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt
frappe.ui.form.on('User Notification Send Message', {
	before_submit:function(frm){
		if(frm.doc.repeat_notification == "Once"){
			frappe.throw("Maaf dokumen ini akan tersubmit ketika sudah tiba waktunya.")
		}
	},
	refresh: function(frm) {
		frm.set_intro("");
		cur_frm.set_intro(__("Dokumen akan terkirim ketika Tanggal dipublish."), true);
			
		if(frm.doc.status == "Sent"){
			cur_frm.fields.forEach(function(l){ cur_frm.set_df_property(l.df.fieldname, "read_only", 1); })
		}
		
		var help_content =
			`<table class="table table-bordered" style="background-color: #f9f9f9;">
				<tr><td>
					<h4>
						<i class="fa fa-hand-right"></i>
						${__('Notes')}
					</h4>
					<ul>
						<li>
							${__("Repeat Function is still develop.")}
						</li>
					</ul>
				</td></tr>
				<tr><td>
					<h4><i class="fa fa-question-sign"></i>
						${__('How this doc works?')}
					</h4>
					<ol>
						<li>
							${__("Create Send Message then it send notification and inbox when on insert")}
						</li>
					</ol>
				</td></tr>
			</table>`;

		frm.set_df_property('instruction', 'options', help_content);

		
		if (cur_frm.is_new()) {
			cur_frm.set_value("status","Not Sent")
			frm.events.repeat_notification(frm)
			var exception = ["status","using_system"]
			cur_frm.fields.forEach(function(l){ 
				if(!exception.includes(l.df.fieldname)){
					cur_frm.set_df_property(l.df.fieldname, "read_only", 0); }})
		}

	},
	repeat_notification: function(frm) {
		if(frm.doc.repeat_notification == "Once"){
		frm.events.make_reqd_property(1)
		}
		else if(frm.doc.repeat_notification == "Now"){
			frm.events.make_reqd_property(0)
			}
			
	},
	// STUB Event Function
	make_reqd_property(reqd_status){
		cur_frm.set_df_property("date_publish","reqd",reqd_status)
		cur_frm.set_df_property("time_publish","reqd",reqd_status)
	}
	

});
