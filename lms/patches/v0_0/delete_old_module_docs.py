import dontmanage


def execute():

	dontmanage.db.delete("DocType", {"module": "Conference"})
	dontmanage.db.delete("DocType", {"module": "Hackathon"})
	dontmanage.db.delete("DocType", {"module": "Event Management"})

	dontmanage.db.delete("Web Form", {"module": "Conference"})
	dontmanage.db.delete("Web Form", {"module": "Hackathon"})
	dontmanage.db.delete("Web Form", {"module": "Event Management"})

	dontmanage.db.delete("Module Def", "Conference")
	dontmanage.db.delete("Module Def", "Hackathon")
	dontmanage.db.delete("Module Def", "Event Management")
