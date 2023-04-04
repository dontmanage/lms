import dontmanage
from dontmanage.model.naming import make_autoname
from dontmanage.model.rename_doc import rename_doc


def execute():
	dontmanage.reload_doc("community", "doctype", "community_member")
	docs = dontmanage.get_all("Community Member")
	for doc in docs:
		member = dontmanage.get_doc("Community Member", doc.name)
		name = make_autoname("hash", "Community Member")
		rename_doc(
			"Community Member",
			member.name,
			name,
			force=True,
			merge=False,
			ignore_permissions=True,
			ignore_if_exists=False,
		)
