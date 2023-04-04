import os

import dontmanage
from dontmanage import _


def execute():
	dontmanage.reload_doc("email", "doctype", "email_template")
	base_path = dontmanage.get_app_path("lms", "templates", "emails")

	if not dontmanage.db.exists("Email Template", _("Mentor Request Creation Template")):
		response = dontmanage.read_file(
			os.path.join(base_path, "mentor_request_creation_email.html")
		)
		dontmanage.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Mentor Request Creation Template"),
				"response": response,
				"subject": _("Request for Mentorship"),
				"owner": dontmanage.session.user,
			}
		).insert(ignore_permissions=True)

		dontmanage.db.set_value(
			"LMS Settings",
			None,
			"mentor_request_creation",
			_("Mentor Request Creation Template"),
		)

	if not dontmanage.db.exists("Email Template", _("Mentor Request Status Update Template")):
		response = dontmanage.read_file(
			os.path.join(base_path, "mentor_request_status_update_email.html")
		)
		dontmanage.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Mentor Request Status Update Template"),
				"response": response,
				"subject": _("The status of your application has changed."),
				"owner": dontmanage.session.user,
			}
		).insert(ignore_permissions=True)

		dontmanage.db.set_value(
			"LMS Settings",
			None,
			"mentor_request_status_update",
			_("Mentor Request Status Update Template"),
		)
