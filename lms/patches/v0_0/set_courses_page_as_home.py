import dontmanage


def execute():
	dontmanage.db.set_value("Portal Settings", None, "default_portal_home", "/courses")
	dontmanage.db.set_value("Role", "Course Instructor", "home_page", "")
	dontmanage.db.set_value("Role", "Course Moderator", "home_page", "")
