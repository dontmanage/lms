import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_certification")
	certificates = dontmanage.get_all("LMS Certification", fields=["name", "student"])
	for certificate in certificates:
		dontmanage.db.set_value(
			"LMS Certification", certificate.name, "member", certificate.student
		)
