import dontmanage
from dontmanage.model.rename_doc import rename_doc


def execute():
	if dontmanage.db.exists("DocType", "LMS Exercise"):
		return

	dontmanage.flags.ignore_route_conflict_validation = True
	rename_doc("DocType", "Exercise", "LMS Exercise")
	dontmanage.flags.ignore_route_conflict_validation = False

	dontmanage.reload_doctype("LMS Exercise", force=True)
