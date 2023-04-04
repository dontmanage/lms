import dontmanage

from lms.lms.utils import get_lesson_url, get_lessons, get_membership


def get_common_context(context):
	context.no_cache = 1

	try:
		batch_name = dontmanage.form_dict["batch"]
	except KeyError:
		batch_name = None

	course = dontmanage.db.get_value(
		"LMS Course",
		dontmanage.form_dict["course"],
		["name", "title", "video_link", "enable_certification", "status"],
		as_dict=True,
	)
	if not course:
		context.template = "www/404.html"
		return
	context.course = course
	context.lessons = get_lessons(course.name)
	membership = get_membership(course.name, dontmanage.session.user, batch_name)
	context.membership = membership
	context.batch = membership.batch if membership and membership.batch else None
	context.course.query_parameter = (
		"?batch=" + membership.batch if membership and membership.batch else ""
	)
	context.livecode_url = get_livecode_url()


def get_livecode_url():
	return dontmanage.db.get_single_value("LMS Settings", "livecode_url")


def redirect_to_lesson(course, index_="1.1"):
	dontmanage.local.flags.redirect_location = (
		get_lesson_url(course.name, index_) + course.query_parameter
	)
	raise dontmanage.Redirect
