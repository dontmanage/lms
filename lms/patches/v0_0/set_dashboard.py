import dontmanage


def execute():
	dontmanage.db.set_value("Portal Settings", None, "default_portal_home", "/users")
