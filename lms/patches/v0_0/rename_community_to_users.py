import dontmanage


def execute():
	doc = dontmanage.db.exists("Top Bar Item", {"url": "/community"})
	if doc:
		dontmanage.db.set_value("Top Bar Item", doc, {"url": "/people", "label": "People"})
