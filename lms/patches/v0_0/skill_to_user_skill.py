import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "user_skill")
	skills = dontmanage.get_all("Skill", pluck="name")

	for skill in skills:
		dontmanage.get_doc({"doctype": "User Skill", "skill": skill}).save()
