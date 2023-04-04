# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document
from dontmanage.utils import cint


class LMSCourseReview(Document):
	pass


@dontmanage.whitelist()
def submit_review(rating, review, course):
	out_of_ratings = dontmanage.db.get_all(
		"DocField", {"parent": "LMS Course Review", "fieldtype": "Rating"}, ["options"]
	)
	out_of_ratings = (len(out_of_ratings) and out_of_ratings[0].options) or 5
	rating = cint(rating) / out_of_ratings
	dontmanage.get_doc(
		{"doctype": "LMS Course Review", "rating": rating, "review": review, "course": course}
	).save(ignore_permissions=True)
	return "OK"
