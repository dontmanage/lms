import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "course_lesson")
	lessons = dontmanage.get_all("Course Lesson", fields=["name", "chapter"])
	for lesson in lessons:
		course = dontmanage.db.get_value("Course Chapter", lesson.chapter, "course")
		dontmanage.db.set_value("Course Lesson", lesson.name, "course", course)
