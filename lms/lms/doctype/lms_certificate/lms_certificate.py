# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import add_years, nowdate
from dontmanage.utils.pdf import get_pdf

from lms.lms.utils import is_certified


class LMSCertificate(Document):
	def before_insert(self):
		certificates = dontmanage.get_all(
			"LMS Certificate", {"member": self.member, "course": self.course}
		)
		if len(certificates):
			full_name = dontmanage.db.get_value("User", self.member, "full_name")
			course_name = dontmanage.db.get_value("LMS Course", self.course, "title")
			dontmanage.throw(
				_("{0} is already certified for the course {1}").format(full_name, course_name)
			)


@dontmanage.whitelist()
def create_certificate(course):
	certificate = is_certified(course)

	if certificate:
		return certificate

	else:
		expires_after_yrs = int(dontmanage.db.get_value("LMS Course", course, "expiry"))
		expiry_date = None
		if expires_after_yrs:
			expiry_date = add_years(nowdate(), expires_after_yrs)

		certificate = dontmanage.get_doc(
			{
				"doctype": "LMS Certificate",
				"member": dontmanage.session.user,
				"course": course,
				"issue_date": nowdate(),
				"expiry_date": expiry_date,
			}
		)
		certificate.save(ignore_permissions=True)
		return certificate


@dontmanage.whitelist()
def get_certificate_pdf(html):
	dontmanage.local.response.filename = "certificate.pdf"
	dontmanage.local.response.filecontent = get_pdf(html, {"orientation": "LandScape"})
	dontmanage.local.response.type = "pdf"
