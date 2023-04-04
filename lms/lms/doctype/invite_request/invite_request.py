# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import json

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils.password import get_decrypted_password


class InviteRequest(Document):
	def on_update(self):
		if self.has_value_changed("status") and self.status == "Approved":
			self.send_email()

	def create_user(self, password):
		full_name_split = self.full_name.split(" ")
		user = dontmanage.get_doc(
			{
				"doctype": "User",
				"email": self.signup_email,
				"first_name": full_name_split[0],
				"last_name": full_name_split[1] if len(full_name_split) > 1 else "",
				"username": self.username,
				"send_welcome_email": 0,
				"user_type": "Website User",
				"new_password": password,
			}
		)
		user.save(ignore_permissions=True)
		return user

	def send_email(self):
		site_name = "Mon.School"
		subject = _("Welcome to {0}!").format(site_name)

		args = {
			"full_name": self.full_name,
			"signup_form_link": f"/new-sign-up?invite_code={self.name}",
			"site_name": site_name,
			"site_url": dontmanage.utils.get_url(),
		}
		dontmanage.sendmail(
			recipients=self.invite_email,
			subject=subject,
			header=[subject, "green"],
			template="lms_invite_request_approved",
			args=args,
			now=True,
		)


@dontmanage.whitelist(allow_guest=True)
def create_invite_request(invite_email):

	if not dontmanage.utils.validate_email_address(invite_email):
		return "invalid email"

	if dontmanage.db.exists("User", invite_email):
		return "user"

	if dontmanage.db.exists("Invite Request", {"invite_email": invite_email}):
		return "invite"

	dontmanage.get_doc(
		{"doctype": "Invite Request", "invite_email": invite_email, "status": "Approved"}
	).save(ignore_permissions=True)
	return "OK"


@dontmanage.whitelist(allow_guest=True)
def update_invite(data):
	data = dontmanage._dict(json.loads(data)) if type(data) == str else dontmanage._dict(data)

	try:
		doc = dontmanage.get_doc("Invite Request", data.invite_code)
	except dontmanage.DoesNotExistError:
		dontmanage.throw(_("Invalid Invite Code."))

	doc.signup_email = data.signup_email
	doc.username = data.username
	doc.full_name = data.full_name
	doc.invite_code = data.invite_code
	doc.save(ignore_permissions=True)

	user = doc.create_user(data.password)
	if user:
		doc.status = "Registered"
		doc.save(ignore_permissions=True)

	return "OK"
