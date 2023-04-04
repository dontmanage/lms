import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_certification")
	dontmanage.reload_doc("lms", "doctype", "lms_certificate")
	old = dontmanage.get_all(
		"LMS Certification", fields=["name", "course", "student", "issue_date", "expiry_date"]
	)
	for data in old:
		dontmanage.get_doc(
			{
				"doctype": "LMS Certificate",
				"course": data.course,
				"member": data.student,
				"issue_date": data.issue_date,
				"expiry_date": data.expiry_date,
			}
		).insert(ignore_permissions=True, ignore_mandatory=True)
