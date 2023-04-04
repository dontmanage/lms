import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_course")
	courses = dontmanage.get_all(
		"LMS Course", {"status": ("is", "not set")}, ["name", "published"]
	)
	for course in courses:
		status = "Approved" if course.published else "In Progress"
		dontmanage.db.set_value("LMS Course", course.name, "status", status)
