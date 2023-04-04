import dontmanage


def execute():
	if (
		dontmanage.db.count("LMS Course")
		and dontmanage.db.count("Course Chapter")
		and dontmanage.db.count("Course Lesson")
		and dontmanage.db.count("LMS Quiz")
	):
		dontmanage.db.set_value("LMS Settings", None, "is_onboarding_complete", True)
