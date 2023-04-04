import dontmanage


def execute():
	table = dontmanage.qb.DocType("Singles")
	q = dontmanage.qb.from_(table).select(table.field).where(table.doctype == "User")
	rows = q.run()

	if len(rows):
		dontmanage.db.delete("Singles", {"doctype": "User"})
