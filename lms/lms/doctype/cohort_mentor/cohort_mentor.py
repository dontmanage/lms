# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class CohortMentor(Document):
	def get_subgroup(self):
		return dontmanage.get_doc("Cohort Subgroup", self.subgroup)

	def get_user(self):
		return dontmanage.get_doc("User", self.email)
