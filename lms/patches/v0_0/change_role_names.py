import dontmanage


def execute():
	if dontmanage.db.exists("Role", "Course Instructor"):
		dontmanage.rename_doc("Role", "Course Instructor", "Instructor")

	if dontmanage.db.exists("Role", "Course Moderator"):
		dontmanage.rename_doc("Role", "Course Moderator", "Moderator")
