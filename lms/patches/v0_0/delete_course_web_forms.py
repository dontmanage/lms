import dontmanage


def execute():
	dontmanage.db.delete("Web Form", "lesson")
	dontmanage.db.delete("Web Form", "chapter")
	dontmanage.db.delete("Web Form", "course")
