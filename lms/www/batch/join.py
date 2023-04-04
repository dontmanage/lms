import dontmanage


def get_context(context):
	context.no_cache = 1
	batch_name = dontmanage.form_dict["batch"]
	context.batch = dontmanage.get_doc("LMS Batch", batch_name)
	context.already_a_member = context.batch.is_member(dontmanage.session.user)
	context.batch.course_title = dontmanage.db.get_value(
		"LMS Course", context.batch.course, "title"
	)
