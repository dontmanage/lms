import dontmanage


def get_context(context):
	try:
		job = dontmanage.form_dict["job"]
	except KeyError:
		dontmanage.local.flags.redirect_location = "/jobs"
		raise dontmanage.Redirect
	context.job = dontmanage.get_doc("Job Opportunity", job)
