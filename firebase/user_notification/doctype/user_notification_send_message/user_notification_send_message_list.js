frappe.listview_settings['User Notification Send Message'] = {
    onload: function (me) {
        frappe.route_options = {
            "destination": "Global",
            "using_system": 0,
        };
        me.page.set_title(__("User Notification Send Message"));
        

    }
}