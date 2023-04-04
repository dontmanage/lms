# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class LessonAssignment(Document):
	def validate(self):
		self.validate_duplicates()

	def validate_duplicates(self):
		if dontmanage.db.exists(
			"Lesson Assignment",
			{"lesson": self.lesson, "member": self.member, "name": ["!=", self.name]},
		):
			lesson_title = dontmanage.db.get_value("Course Lesson", self.lesson, "title")
			dontmanage.throw(
				_("Assignment for Lesson {0} by {1} already exists.").format(
					lesson_title, self.member_name
				)
			)


@dontmanage.whitelist()
def upload_assignment(assignment, lesson):
	args = {
		"doctype": "Lesson Assignment",
		"lesson": lesson,
		"member": dontmanage.session.user,
	}
	if dontmanage.db.exists(args):
		del args["doctype"]
		dontmanage.db.set_value("Lesson Assignment", args, "assignment", assignment)
	else:
		args.update({"assignment": assignment})
		lesson_work = dontmanage.get_doc(args)
		lesson_work.save(ignore_permissions=True)


@dontmanage.whitelist()
def get_assignment(lesson):
	assignment = dontmanage.db.get_value(
		"Lesson Assignment",
		{"lesson": lesson, "member": dontmanage.session.user},
		["lesson", "member", "assignment", "comments", "status"],
		as_dict=True,
	)
	assignment.file_name = dontmanage.db.get_value(
		"File", {"file_url": assignment.assignment}, "file_name"
	)
	return assignment


@dontmanage.whitelist()
def grade_assignment(name, result, comments):
	doc = dontmanage.get_doc("Lesson Assignment", name)
	doc.status = result
	doc.comments = comments
	doc.save(ignore_permissions=True)
