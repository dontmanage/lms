import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_course")
	courses = dontmanage.get_all("LMS Course", fields=["name", "owner"])
	for course in courses:
		dontmanage.db.set_value("LMS Course", course.name, "instructor", course.owner)
