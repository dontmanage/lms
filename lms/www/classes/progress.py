import dontmanage
from lms.lms.utils import has_course_moderator_role
from dontmanage import _


def get_context(context):
	context.no_cache = 1

	student = dontmanage.form_dict["username"]
	classname = dontmanage.form_dict["classname"]
	context.is_moderator = has_course_moderator_role()

	context.student = dontmanage.db.get_value(
		"User",
		{"username": student},
		["first_name", "full_name", "name", "last_active", "username"],
		as_dict=True,
	)
	context.class_info = dontmanage.db.get_value(
		"LMS Class", classname, ["name"], as_dict=True
	)

	class_courses = dontmanage.get_all(
		"Class Course", {"parent": classname}, ["course", "title"]
	)

	for course in class_courses:
		course.membership = dontmanage.db.get_value(
			"LMS Batch Membership",
			{"member": context.student.name, "course": course.course},
			["progress"],
			as_dict=True,
		)
		course.quizzes = dontmanage.get_all(
			"LMS Quiz", {"course": course.course}, ["name", "title"]
		)
		course.assignments = dontmanage.get_all(
			"Course Lesson",
			{"course": course.course, "question": ["is", "set"]},
			["name", "title"],
		)
		course.evaluations = dontmanage.get_all(
			"LMS Certificate Evaluation",
			{"course": course.course, "member": context.student.name},
			["rating", "status", "creation", "name"],
		)

	context.class_courses = class_courses
