import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "course_chapter")
	dontmanage.reload_doc("lms", "doctype", "course_lesson")
	dontmanage.reload_doc("lms", "doctype", "chapter_reference")
	dontmanage.reload_doc("lms", "doctype", "lesson_reference")
	dontmanage.reload_doc("lms", "doctype", "exercise")
	dontmanage.reload_doc("lms", "doctype", "exercise_submission")
	dontmanage.reload_doc("lms", "doctype", "lms_batch_membership")
	dontmanage.reload_doc("lms", "doctype", "lms_course")
	dontmanage.reload_doc("lms", "doctype", "lms_course_progress")
	dontmanage.reload_doc("lms", "doctype", "lms_quiz")

	if not dontmanage.db.count("Course Chapter"):
		move_chapters()

	if not dontmanage.db.count("Course Lesson"):
		move_lessons()

	change_parent_for_lesson_reference()


def move_chapters():
	docs = dontmanage.get_all("Chapter", fields=["*"])
	for doc in docs:
		if dontmanage.db.exists("LMS Course", doc.course):
			name = doc.name
			doc.update({"doctype": "Course Chapter"})
			del doc["name"]
			new_doc = dontmanage.get_doc(doc)
			new_doc.save()
			dontmanage.rename_doc("Course Chapter", new_doc.name, name)


def move_lessons():
	docs = dontmanage.get_all("Lesson", fields=["*"])
	for doc in docs:
		if dontmanage.db.exists("Chapter", doc.chapter):
			name = doc.name
			doc.update({"doctype": "Course Lesson"})
			del doc["name"]
			new_doc = dontmanage.get_doc(doc)
			new_doc.save()
			dontmanage.rename_doc("Course Lesson", new_doc.name, name)


def change_parent_for_lesson_reference():
	lesson_reference = dontmanage.get_all("Lesson Reference", fields=["name", "parent"])
	for reference in lesson_reference:
		dontmanage.db.set_value(
			"Lesson Reference", reference.name, "parenttype", "Course Chapter"
		)
