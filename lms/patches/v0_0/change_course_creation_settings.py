import dontmanage


def execute():
	value = dontmanage.db.get_single_value("LMS Settings", "portal_course_creation")
	if value == "Course Instructor Role":
		dontmanage.db.set_value(
			"LMS Settings", None, "portal_course_creation", "Course Creator Role"
		)
