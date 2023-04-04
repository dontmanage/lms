import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_course")
	dontmanage.reload_doc("lms", "doctype", "chapter")
	dontmanage.reload_doc("lms", "doctype", "lesson")
	dontmanage.reload_doc("lms", "doctype", "lessons")
	dontmanage.reload_doc("lms", "doctype", "chapters")

	update_chapters()
	update_lessons()


def update_chapters():
	courses = dontmanage.get_all("LMS Course", pluck="name")
	for course in courses:
		course_details = dontmanage.get_doc("LMS Course", course)
		chapters = dontmanage.get_all("Chapter", {"course": course}, ["name"], order_by="index_")
		for chapter in chapters:
			course_details.append("chapters", {"chapter": chapter.name})

		course_details.save()


def update_lessons():
	chapters = dontmanage.get_all("Chapter", pluck="name")
	for chapter in chapters:
		chapter_details = dontmanage.get_doc("Chapter", chapter)
		lessons = dontmanage.get_all("Lesson", {"chapter": chapter}, ["name"], order_by="index_")
		for lesson in lessons:
			chapter_details.append("lessons", {"lesson": lesson.name})

		chapter_details.save()
