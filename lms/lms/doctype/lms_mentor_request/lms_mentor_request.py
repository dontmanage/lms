# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class LMSMentorRequest(Document):
	def on_update(self):
		if self.has_value_changed("status"):

			if self.status == "Approved":
				self.create_course_mentor_mapping()

			if self.status != "Pending":
				self.send_status_change_email()

	def create_course_mentor_mapping(self):
		mapping = dontmanage.get_doc(
			{
				"doctype": "LMS Course Mentor Mapping",
				"mentor": self.member,
				"course": self.course,
			}
		)
		mapping.save()

	def send_creation_email(self):
		email_template = self.get_email_template("mentor_request_creation")
		if not email_template:
			return

		course_details = dontmanage.db.get_value(
			"LMS Course", self.course, ["owner", "slug", "title"], as_dict=True
		)
		message = dontmanage.render_template(
			email_template.response,
			{
				"member_name": dontmanage.db.get_value("User", dontmanage.session.user, "full_name"),
				"course_url": "/courses/" + course_details.slug,
				"course": course_details.title,
			},
		)

		email_args = {
			"recipients": [dontmanage.session.user, course_details.owner],
			"subject": email_template.subject,
			"header": email_template.subject,
			"message": message,
		}
		dontmanage.enqueue(
			method=dontmanage.sendmail, queue="short", timeout=300, is_async=True, **email_args
		)

	def send_status_change_email(self):
		email_template = self.get_email_template("mentor_request_status_update")
		if not email_template:
			return

		course_details = dontmanage.db.get_value(
			"LMS Course", self.course, ["owner", "title"], as_dict=True
		)
		message = dontmanage.render_template(
			email_template.response,
			{
				"member_name": self.member_name,
				"status": self.status,
				"course": course_details.title,
			},
		)

		if self.status == "Approved" or self.status == "Rejected":
			email_args = {
				"recipients": self.member,
				"cc": [course_details.owner, self.reviewed_by],
				"subject": email_template.subject,
				"header": email_template.subject,
				"message": message,
			}
			dontmanage.enqueue(
				method=dontmanage.sendmail, queue="short", timeout=300, is_async=True, **email_args
			)

		elif self.status == "Withdrawn":
			email_args = {
				"recipients": [self.member, course_details.owner],
				"subject": email_template.subject,
				"header": email_template.subject,
				"message": message,
			}
			dontmanage.enqueue(
				method=dontmanage.sendmail, queue="short", timeout=300, is_async=True, **email_args
			)

	def get_email_template(self, template_name):
		template = dontmanage.db.get_single_value("LMS Settings", template_name)
		if template:
			return dontmanage.get_doc("Email Template", template)


@dontmanage.whitelist()
def has_requested(course):
	return dontmanage.db.count(
		"LMS Mentor Request",
		filters={
			"member": dontmanage.session.user,
			"course": course,
			"status": ["in", ("Pending", "Approved")],
		},
	)


@dontmanage.whitelist()
def create_request(course):
	if not has_requested(course):
		request = dontmanage.get_doc(
			{
				"doctype": "LMS Mentor Request",
				"member": dontmanage.session.user,
				"course": course,
				"status": "Pending",
			}
		)
		request.save(ignore_permissions=True)
		request.send_creation_email()
		return "OK"

	else:
		return "Already Applied"


@dontmanage.whitelist()
def cancel_request(course):
	request = dontmanage.get_doc(
		"LMS Mentor Request",
		{
			"member": dontmanage.session.user,
			"course": course,
			"status": ["in", ("Pending", "Approved")],
		},
	)
	request.status = "Withdrawn"
	request.save(ignore_permissions=True)
	return "OK"
