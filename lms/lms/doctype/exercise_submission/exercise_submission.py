# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class ExerciseSubmission(Document):
	def on_update(self):
		self.update_latest_submission()

	def update_latest_submission(self):
		names = dontmanage.get_all(
			"Exercise Latest Submission", {"exercise": self.exercise, "member": self.member}
		)
		if names:
			doc = dontmanage.get_doc("Exercise Latest Submission", names[0])
			doc.latest_submission = self.name
			doc.save(ignore_permissions=True)
		else:
			doc = dontmanage.get_doc(
				{
					"doctype": "Exercise Latest Submission",
					"exercise": self.exercise,
					"member": self.member,
					"latest_submission": self.name,
				}
			)
			doc.insert(ignore_permissions=True)
