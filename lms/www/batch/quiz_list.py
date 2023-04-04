import dontmanage


def get_context(context):
	context.no_cache = 1
	context.quiz_list = dontmanage.get_all(
		"LMS Quiz", {"owner": dontmanage.session.user}, ["name", "title"]
	)
