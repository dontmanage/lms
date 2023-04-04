# Copyright (c) 2022, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class CourseEvaluator(Document):
	def validate(self):
		self.validate_time_slots()

	def validate_time_slots(self):
		for schedule in self.schedule:
			if schedule.start_time >= schedule.end_time:
				dontmanage.throw(_("Start Time cannot be greater than End Time"))

			self.validate_overlaps(schedule)

	def validate_overlaps(self, schedule):
		same_day_slots = list(
			filter(lambda x: x.day == schedule.day and x.name != schedule.name, self.schedule)
		)
		overlap = False

		for slot in same_day_slots:
			if schedule.start_time <= slot.start_time < schedule.end_time:
				overlap = True
			if schedule.start_time < slot.end_time <= schedule.end_time:
				overlap = True
			if slot.start_time < schedule.start_time and schedule.end_time < slot.end_time:
				overlap = True

			if overlap:
				dontmanage.throw(_("Slot Times are overlapping for some schedules."))


@dontmanage.whitelist()
def get_schedule(course, date):
	evaluator = dontmanage.db.get_value("LMS Course", course, "evaluator")
	all_slots = dontmanage.get_all(
		"Evaluator Schedule",
		filters={"parent": evaluator},
		fields=["day", "start_time", "end_time"],
	)
	booked_slots = dontmanage.get_all(
		"LMS Certificate Request",
		filters={"evaluator": evaluator, "date": date},
		fields=["start_time"],
	)

	for slot in booked_slots:
		same_slot = list(filter(lambda x: x.start_time == slot.start_time, all_slots))
		if len(same_slot):
			all_slots.remove(same_slot[0])

	return all_slots
