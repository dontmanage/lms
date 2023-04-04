# Copyright (c) 2023, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document
from datetime import timedelta
from dontmanage.utils import cint, get_datetime


class LMSLiveClass(Document):
	def after_insert(self):
		calendar = dontmanage.db.get_value(
			"Google Calendar", {"user": dontmanage.session.user, "enable": 1}, "name"
		)

		if calendar:
			event = self.create_event()
			self.add_event_participants(event, calendar)

	def create_event(self):
		start = f"{self.date} {self.time}"

		event = dontmanage.get_doc(
			{
				"doctype": "Event",
				"subject": f"Live Class on {self.title}",
				"starts_on": start,
				"ends_on": get_datetime(start) + timedelta(minutes=cint(self.duration)),
			}
		)
		event.save()

		return event

	def add_event_participants(self, event, calendar):
		participants = dontmanage.get_all(
			"Class Student", {"parent": self.class_name}, pluck="student"
		)

		participants.append(dontmanage.session.user)
		for participant in participants:
			dontmanage.get_doc(
				{
					"doctype": "Event Participants",
					"reference_doctype": "User",
					"reference_docname": participant,
					"email": participant,
					"parent": event.name,
					"parenttype": "Event",
					"parentfield": "event_participants",
				}
			).save()

		event.reload()
		event.update(
			{
				"sync_with_google_calendar": 1,
				"google_calendar": calendar,
				"description": f"A Live Class has been scheduled on {dontmanage.utils.format_date(self.date, 'medium')} at { dontmanage.utils.format_time(self.time, 'hh:mm a')}. Click on this link to join. {self.join_url}. {self.description}",
			}
		)

		event.save()
