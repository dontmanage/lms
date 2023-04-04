import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_course")
	dontmanage.reload_doc("lms", "doctype", "course_instructor")
	courses = dontmanage.get_all("LMS Course", fields=["name", "instructor"])
	for course in courses:
		doc = dontmanage.get_doc(
			{
				"doctype": "Course Instructor",
				"parent": course.name,
				"parentfield": "instructors",
				"parenttype": "LMS Course",
				"instructor": course.instructor,
			}
		)
		doc.save()
