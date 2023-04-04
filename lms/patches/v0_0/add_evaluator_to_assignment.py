import dontmanage


def execute():
	assignments = dontmanage.get_all("Lesson Assignment", fields=["name", "course"])
	for assignment in assignments:
		evaluator = dontmanage.db.get_value("LMS Course", assignment.course, "evaluator")
		dontmanage.db.set_value("Lesson Assignment", assignment.name, "evaluator", evaluator)
