import dontmanage


def execute():
	dontmanage.reload_doc("community", "doctype", "community_member")
	docs = dontmanage.get_all("Community Member")
	for doc in docs:
		member = dontmanage.get_doc("Community Member", doc.name)
		if not member.abbr:
			abbr = ("").join([s[0] for s in member.full_name.split()])
			dontmanage.db.set_value("Community Member", member.name, "abbr", abbr)
