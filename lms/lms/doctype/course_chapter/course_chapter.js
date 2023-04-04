// Copyright (c) 2021, FOSS United and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("Course Chapter", {
	onload: function (frm) {
		frm.set_query("lesson", "lessons", function () {
			return {
				filters: {
					chapter: frm.doc.name,
				},
			};
		});
	},
});
