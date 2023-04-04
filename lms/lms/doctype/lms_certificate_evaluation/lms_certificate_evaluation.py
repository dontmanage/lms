# Copyright (c) 2022, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document
from dontmanage.model.mapper import get_mapped_doc
from lms.lms.utils import has_course_moderator_role


class LMSCertificateEvaluation(Document):
	pass


def has_website_permission(doc, ptype, user, verbose=False):
	if has_course_moderator_role() or doc.member == dontmanage.session.user:
		return True
	return False


@dontmanage.whitelist()
def create_lms_certificate(source_name, target_doc=None):
	doc = get_mapped_doc(
		"LMS Certificate Evaluation",
		source_name,
		{"LMS Certificate Evaluation": {"doctype": "LMS Certificate"}},
		target_doc,
	)
	return doc
