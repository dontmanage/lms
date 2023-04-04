# Copyright (c) 2021, FOSS United and Contributors
# See license.txt

# import dontmanage
import unittest

import dontmanage


class TestLMSQuiz(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		dontmanage.get_doc({"doctype": "LMS Quiz", "title": "Test Quiz"}).save(
			ignore_permissions=True
		)

	def test_with_multiple_options(self):
		quiz = dontmanage.get_doc("LMS Quiz", "test-quiz")
		quiz.append(
			"questions",
			{
				"question": "Question Multiple",
				"type": "Choices",
				"option_1": "Option 1",
				"is_correct_1": 1,
				"option_2": "Option 2",
				"is_correct_2": 1,
			},
		)
		quiz.save()
		self.assertTrue(quiz.questions[0].multiple)

	def test_with_no_correct_option(self):
		quiz = dontmanage.get_doc("LMS Quiz", "test-quiz")
		quiz.append(
			"questions",
			{
				"question": "Question no correct option",
				"type": "Choices",
				"option_1": "Option 1",
				"option_2": "Option 2",
			},
		)
		self.assertRaises(dontmanage.ValidationError, quiz.save)

	def test_with_no_possible_answers(self):
		quiz = dontmanage.get_doc("LMS Quiz", "test-quiz")
		quiz.append(
			"questions",
			{
				"question": "Question Possible Answers",
				"type": "User Input",
			},
		)
		self.assertRaises(dontmanage.ValidationError, quiz.save)

	@classmethod
	def tearDownClass(cls) -> None:
		dontmanage.db.delete("LMS Quiz", "test-quiz")
		dontmanage.db.delete("LMS Quiz Question", {"parent": "test-quiz"})
