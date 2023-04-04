import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_course_mentor_mapping")
	mappings = dontmanage.get_all("LMS Course Mentor Mapping", ["mentor", "name"])
	for mapping in mappings:
		email = dontmanage.db.get_value("Community Member", mapping.mentor, "email")
		dontmanage.db.set_value("LMS Course Mentor Mapping", mapping.name, "mentor", email)
