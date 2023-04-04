import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_quiz_submission")
	submissions = dontmanage.db.get_all("LMS Quiz Submission", fields=["name", "owner"])

	for submission in submissions:
		dontmanage.db.set_value(
			"LMS Quiz Submission", submission.name, "member", submission.owner
		)
