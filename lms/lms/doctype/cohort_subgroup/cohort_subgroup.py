# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document
from dontmanage.utils import random_string


class CohortSubgroup(Document):
	def before_save(self):
		if not self.invite_code:
			self.invite_code = random_string(8)

	def get_url(self):
		cohort = dontmanage.get_doc("Cohort", self.cohort)
		return (
			f"{dontmanage.utils.get_url()}/courses/{self.course}/subgroups/{cohort.slug}/{self.slug}"
		)

	def get_invite_link(self):
		cohort = dontmanage.get_doc("Cohort", self.cohort)
		return f"{dontmanage.utils.get_url()}/courses/{self.course}/join/{cohort.slug}/{self.slug}/{self.invite_code}"

	def has_student(self, email):
		"""Check if given user is a student of this subgroup."""
		q = {"doctype": "LMS Batch Membership", "subgroup": self.name, "member": email}
		return dontmanage.db.exists(q)

	def has_join_request(self, email):
		"""Check if given user is a student of this subgroup."""
		q = {"doctype": "Cohort Join Request", "subgroup": self.name, "email": email}
		return dontmanage.db.exists(q)

	def get_join_requests(self, status="Pending"):
		q = {"subgroup": self.name, "status": status}
		return dontmanage.get_all(
			"Cohort Join Request", filters=q, fields=["*"], order_by="creation desc"
		)

	def get_mentors(self):
		emails = dontmanage.get_all(
			"Cohort Mentor", filters={"subgroup": self.name}, fields=["email"], pluck="email"
		)
		return self._get_users(emails)

	def get_students(self):
		emails = dontmanage.get_all(
			"LMS Batch Membership",
			filters={"subgroup": self.name},
			fields=["member"],
			pluck="member",
			page_length=1000,
		)
		return self._get_users(emails)

	def _get_users(self, emails):
		users = [dontmanage.get_cached_doc("User", email) for email in emails]
		return sorted(users, key=lambda user: user.full_name)

	def is_mentor(self, email):
		q = {"doctype": "Cohort Mentor", "subgroup": self.name, "email": email}
		return dontmanage.db.exists(q)

	def is_manager(self, email):
		"""Returns True if the given user is a manager of this subgroup.

		Mentors of the subgroup, admins of the Cohort are considered as managers.
		"""
		return self.is_mentor(email) or self.get_cohort().is_admin(email)

	def get_cohort(self):
		return dontmanage.get_doc("Cohort", self.cohort)

	def add_mentor(self, email):
		d = {
			"doctype": "Cohort Mentor",
			"subgroup": self.name,
			"cohort": self.cohort,
			"email": email,
		}
		if dontmanage.db.exists(d):
			return
		doc = dontmanage.get_doc(d)
		doc.insert(ignore_permissions=True)


# def after_doctype_insert():
#    dontmanage.db.add_unique("Cohort Subgroup", ("cohort", "slug"))
