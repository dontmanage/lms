# Copyright (c) 2021, FOSS United and Contributors
# See license.txt

import unittest

import dontmanage

from lms.lms.doctype.lms_course.test_lms_course import new_course


class TestLMSExercise(unittest.TestCase):
	def new_exercise(self):
		course = new_course("Test Course")
		member = dontmanage.get_doc(
			{
				"doctype": "LMS Batch Membership",
				"course": course.name,
				"member": dontmanage.session.user,
			}
		)
		member.insert()
		e = dontmanage.get_doc(
			{
				"doctype": "LMS Exercise",
				"name": "test-problem",
				"course": course.name,
				"title": "Test Problem",
				"description": "draw a circle",
				"code": "# draw a single cicle",
				"answer": ("# draw a single circle\n" + "circle(100, 100, 50)"),
			}
		)
		e.insert()
		return e

	def test_exercise(self):
		e = self.new_exercise()
		assert e.get_user_submission() is None

	def test_exercise_submission(self):
		e = self.new_exercise()
		submission = e.submit("circle(100, 100, 50)")
		assert submission is not None
		assert submission.exercise == e.name
		assert submission.course == e.course

		user_submission = e.get_user_submission()
		assert user_submission is not None
		assert user_submission.name == submission.name

	def tearDown(self):
		dontmanage.db.sql("delete from `tabLMS Batch Membership`")
		dontmanage.db.sql("delete from `tabExercise Submission`")
		dontmanage.db.sql("delete from `tabLMS Exercise`")
