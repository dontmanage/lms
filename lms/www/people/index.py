import dontmanage


def get_context(context):
	context.user_count = dontmanage.db.count("User", {"enabled": True})
	context.users = dontmanage.get_all(
		"User",
		filters={"enabled": True},
		fields=["name", "username", "full_name", "user_image", "headline", "looking_for_job"],
		start=0,
		page_length=24,
		order_by="creation desc",
	)
