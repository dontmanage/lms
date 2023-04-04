import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_quiz_submission")
	dontmanage.reload_doc("lms", "doctype", "lms_quiz_result")
	results = dontmanage.get_all("LMS Quiz Result", fields=["name", "result"])

	for result in results:
		value = 1 if result.result == "Right" else 0
		dontmanage.db.set_value("LMS Quiz Result", result.name, "is_correct", value)
