import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_course_progress")
	progress_records = dontmanage.get_all(
		"LMS Course Progress", fields=["name", "owner", "member"]
	)

	for progress in progress_records:
		if not progress.member:
			full_name = dontmanage.db.get_value("User", progress.owner, "full_name")
			dontmanage.db.set_value("LMS Course Progress", progress.name, "member", progress.owner)
			dontmanage.db.set_value("LMS Course Progress", progress.name, "member_name", full_name)
