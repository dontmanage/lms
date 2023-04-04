# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class LMSCourseInterest(Document):
	pass


@dontmanage.whitelist()
def capture_interest(course):
	data = {
		"doctype": "LMS Course Interest",
		"course": course,
		"user": dontmanage.session.user,
	}
	if not dontmanage.db.exists(data):
		dontmanage.get_doc(data).save(ignore_permissions=True)
	return "OK"
