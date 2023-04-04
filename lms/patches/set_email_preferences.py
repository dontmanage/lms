import dontmanage


def execute():
	dontmanage.reload_doc("community", "doctype", "community_member")
	members = dontmanage.get_all("Community Member", ["name", "email_preference"])
	for member in members:
		if not member.email_preference:
			dontmanage.db.set_value(
				"Community Member", member.name, "email_preference", "Email on every Message"
			)
