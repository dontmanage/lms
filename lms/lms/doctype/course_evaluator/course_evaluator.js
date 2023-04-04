// Copyright (c) 2022, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("Course Evaluator", {
	onload: (frm) => {
		frm.set_query("evaluator", function (doc) {
			return {
				filters: {
					ignore_user_type: 1,
				},
			};
		});
	},
});
