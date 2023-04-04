import dontmanage
from lms.lms.utils import has_course_moderator_role
from dontmanage import _


def get_context(context):
	context.no_cache = 1
	assignment = dontmanage.form_dict["assignment"]

	context.assignment = dontmanage.db.get_value(
		"Lesson Assignment",
		assignment,
		[
			"assignment",
			"comments",
			"status",
			"name",
			"member",
			"member_name",
			"course",
			"lesson",
		],
		as_dict=True,
	)
	context.is_moderator = has_course_moderator_role()

	if (
		not has_course_moderator_role()
		and not dontmanage.session.user == context.assignment.member
	):
		message = "You don't have the permissions to access this page."
		if dontmanage.session.user == "Guest":
			message = "Please login to access this page."

		raise dontmanage.PermissionError(_(message))
