import dontmanage
from dontmanage.utils import rounded

from lms.lms.utils import get_course_progress


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_batch_membership")
	memberships = dontmanage.get_all(
		"LMS Batch Membership", ["name", "course", "member"], order_by="course"
	)

	if len(memberships):
		current_course = memberships[0].course
		for membership in memberships:
			if current_course != membership.course:
				current_course = membership.course

			progress = rounded(get_course_progress(current_course, membership.member))
			dontmanage.db.set_value("LMS Batch Membership", membership.name, "progress", progress)

	dontmanage.db.delete("Prepared Report", {"ref_report_doctype": "Course Progress Summary"})
	dontmanage.db.set_value("Report", "Course Progress Summary", "prepared_report", 0)
