// Copyright (c) 2021, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('User Notification Settings', {
	refresh: function(frm) {
		frm.set_intro(__(`
		Mohon maaf, fungsi ini belum diimplementasikan ke Send Message. 
		<br> Don't forget to fill key in <a href='/desk#Form/Firebase%20Setting/Firebase%20Setting'> Firebase Settings </a>.`), true);
	}
});
