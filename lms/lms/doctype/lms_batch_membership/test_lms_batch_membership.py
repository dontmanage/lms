# Copyright (c) 2021, FOSS United and Contributors
# See license.txt

import unittest

import dontmanage

from lms.lms.doctype.lms_course.test_lms_course import new_course, new_user


class TestLMSBatchMembership(unittest.TestCase):
	def setUp(self):
		dontmanage.db.sql("DELETE FROM `tabLMS Batch Membership`")
		dontmanage.db.sql("DELETE FROM `tabLMS Batch`")
		dontmanage.db.sql("delete from `tabLMS Course Mentor Mapping`")
		dontmanage.db.sql("DELETE FROM `tabUser` where email like '%@test.com'")

	def new_course_batch(self):
		course = new_course("Test Course")

		new_user("Test Mentor", "mentor@test.com")
		# without this, the creating batch will fail
		course.add_mentor("mentor@test.com")

		dontmanage.session.user = "mentor@test.com"

		batch = dontmanage.get_doc(
			{
				"doctype": "LMS Batch",
				"name": "test-batch",
				"title": "Test Batch",
				"course": course.name,
			}
		)
		batch.insert(ignore_permissions=True)

		dontmanage.session.user = "Administrator"
		return course, batch

	def add_membership(self, batch_name, member_name, member_type="Student"):
		doc = dontmanage.get_doc(
			{
				"doctype": "LMS Batch Membership",
				"batch": batch_name,
				"member": member_name,
				"member_type": member_type,
			}
		)
		doc.insert()
		return doc

	def test_membership(self):
		course, batch = self.new_course_batch()
		member = new_user("Test", "test01@test.com")
		membership = self.add_membership(batch.name, member.name)

		assert membership.course == course.name
		assert membership.member_name == member.full_name

	def test_membership_change_role(self):
		course, batch = self.new_course_batch()
		member = new_user("Test", "test01@test.com")
		membership = self.add_membership(batch.name, member.name)

		# it should be possible to change role
		membership.role = "Admin"
		membership.save()
