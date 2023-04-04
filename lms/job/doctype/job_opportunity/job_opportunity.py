# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import get_link_to_form
from dontmanage.utils.user import get_system_managers

from lms.lms.utils import validate_image


class JobOpportunity(Document):
	def validate(self):
		self.validate_urls()
		self.company_logo = validate_image(self.company_logo)

	def validate_urls(self):
		dontmanage.utils.validate_url(self.company_website, True)
		dontmanage.utils.validate_url(self.application_link, True)


@dontmanage.whitelist()
def report(job, reason):
	system_managers = get_system_managers(only_name=True)
	user = dontmanage.db.get_value("User", dontmanage.session.user, "full_name")
	subject = _("User {0} has reported the job post {1}").format(user, job)
	args = {
		"job": job,
		"job_url": get_link_to_form("Job Opportunity", job),
		"user": user,
		"reason": reason,
	}
	dontmanage.sendmail(
		recipients=system_managers,
		subject=subject,
		header=[subject, "green"],
		template="job_report",
		args=args,
		now=True,
	)
