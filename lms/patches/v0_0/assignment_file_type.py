import dontmanage


def execute():
	assignment_lessons = dontmanage.get_all(
		"Course Lesson", {"file_type": ["is", "set"]}, ["name", "question"]
	)

	for lesson in assignment_lessons:
		if not lesson.question:
			dontmanage.db.set_value("Course Lesson", lesson.name, "file_type", "")
