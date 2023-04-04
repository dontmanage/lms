// Copyright (c) 2021, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("Job Opportunity", {
	refresh: (frm) => {
		if (frm.doc.name)
			frm.add_web_link(`/jobs/${frm.doc.name}`, "See on Website");
	},
});
