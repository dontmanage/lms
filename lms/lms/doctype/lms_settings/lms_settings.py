# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import get_url_to_list


class LMSSettings(Document):
	def validate(self):
		self.validate_google_settings()

	def validate_google_settings(self):
		if self.send_calendar_invite_for_evaluations:
			google_settings = dontmanage.get_single("Google Settings")

			if not google_settings.enable:
				dontmanage.throw(
					_("Enable Google API in Google Settings to send calendar invites for evaluations.")
				)

			if not google_settings.client_id or not google_settings.client_secret:
				dontmanage.throw(
					_(
						"Enter Client Id and Client Secret in Google Settings to send calendar invites for evaluations."
					)
				)

			calendars = dontmanage.db.count("Google Calendar")
			if not calendars:
				dontmanage.throw(
					_(
						"Please add <a href='{0}'>{1}</a> for <a href='{2}'>{3}</a> to send calendar invites for evaluations."
					).format(
						get_url_to_list("Google Calendar"),
						dontmanage.bold("Google Calendar"),
						get_url_to_list("Course Evaluator"),
						dontmanage.bold("Course Evaluator"),
					)
				)
