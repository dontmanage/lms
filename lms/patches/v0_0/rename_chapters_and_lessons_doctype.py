import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_course")
	dontmanage.reload_doc("lms", "doctype", "chapter")
	dontmanage.reload_doc("lms", "doctype", "lesson")
	dontmanage.reload_doc("lms", "doctype", "chapter_reference")
	dontmanage.reload_doc("lms", "doctype", "lesson_reference")

	if not dontmanage.db.count("Chapter Reference"):
		move_chapters()

	if not dontmanage.db.count("Lesson Reference"):
		move_lessons()


def move_chapters():
	docs = dontmanage.get_all("Chapters", fields=["*"])
	for doc in docs:
		keys = doc
		keys.update({"doctype": "Chapter Reference"})
		del keys["name"]
		dontmanage.get_doc(keys).save()


def move_lessons():
	docs = dontmanage.get_all("Lessons", fields=["*"])
	for doc in docs:
		keys = doc
		keys.update({"doctype": "Lesson Reference"})
		del keys["name"]
		dontmanage.get_doc(keys).save()
