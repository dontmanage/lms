import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_message")
	messages = dontmanage.get_all("LMS Message", ["author", "name"])
	for message in messages:
		user = dontmanage.db.get_value(
			"Community Member", message.author, ["email", "full_name"], as_dict=True
		)
		dontmanage.db.set_value("LMS Message", message.name, "author", user.email)
		dontmanage.db.set_value("LMS Message", message.name, "author_name", user.full_name)
