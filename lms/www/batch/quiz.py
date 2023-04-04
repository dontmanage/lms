import dontmanage
from dontmanage.utils import cstr


def get_context(context):
	context.no_cache = 1
	quizname = dontmanage.form_dict["quizname"]
	if quizname == "new-quiz":
		context.quiz = dontmanage._dict()
		context.quiz.edit_mode = 1
	else:
		fields_arr = ["name", "question", "type"]
		for num in range(1, 5):
			fields_arr.append("option_" + cstr(num))
			fields_arr.append("is_correct_" + cstr(num))
			fields_arr.append("explanation_" + cstr(num))
			fields_arr.append("possibility_" + cstr(num))

		context.quiz = dontmanage.db.get_value("LMS Quiz", quizname, ["title", "name"], as_dict=1)
		context.quiz.questions = dontmanage.get_all(
			"LMS Quiz Question", {"parent": quizname}, fields_arr, order_by="idx"
		)
