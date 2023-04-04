import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_mentor_request")
	requests = dontmanage.get_all("LMS Mentor Request", ["member", "name"])
	for request in requests:
		user = dontmanage.db.get_value(
			"Community Member", request.member, ["email", "full_name"], as_dict=True
		)
		dontmanage.db.set_value("LMS Mentor Request", request.name, "member", user.email)
		dontmanage.db.set_value("LMS Mentor Request", request.name, "member_name", user.full_name)
