import dontmanage
from dontmanage.utils import flt


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_course_progress")
	progress_records = dontmanage.get_all("LMS Batch Membership", fields=["name", "progress"])
	for progress in progress_records:
		dontmanage.db.set_value(
			"LMS Batch Membership", progress.name, "progress", flt(progress.progress)
		)
