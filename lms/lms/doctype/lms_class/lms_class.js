// Copyright (c) 2022, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("LMS Class", {
	onload: function (frm) {
		frm.set_query("student", "students", function (doc) {
			return {
				filters: {
					ignore_user_type: 1,
				},
			};
		});
	},
});
