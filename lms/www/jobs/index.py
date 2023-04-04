import dontmanage


def get_context(context):
	context.jobs = dontmanage.get_all(
		"Job Opportunity",
		{"status": "Open", "disabled": False},
		["job_title", "location", "type", "company_name", "company_logo", "name", "creation"],
		order_by="creation desc",
	)
	context.title = dontmanage.db.get_single_value("Job Settings", "title")
	context.subtitle = dontmanage.db.get_single_value("Job Settings", "subtitle")
	context.allow_posting = dontmanage.db.get_single_value("Job Settings", "allow_posting")
