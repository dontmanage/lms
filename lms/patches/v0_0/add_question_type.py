import dontmanage


def execute():
	questions = dontmanage.get_all("LMS Quiz Question", pluck="name")

	for question in questions:
		dontmanage.db.set_value("LMS Quiz Question", question, "type", "Choices")
