import dontmanage


def execute():
	dontmanage.reload_doc("lms", "doctype", "lms_batch_membership")
	memberships = dontmanage.get_all("LMS Batch Membership", ["member", "name"])
	for membership in memberships:
		email = dontmanage.db.get_value("Community Member", membership.member, "email")
		dontmanage.db.set_value("LMS Batch Membership", membership.name, "member", email)
