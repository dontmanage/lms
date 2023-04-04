import dontmanage
from dontmanage.utils.jinja import render_template

from lms.lms.utils import get_instructors


def get_context(context):
	context.no_cache = 1

	try:
		course_name = dontmanage.form_dict["course"]
		certificate_name = dontmanage.form_dict["certificate"]
	except KeyError:
		redirect_to_course_list()

	context.certificate = dontmanage.db.get_value(
		"LMS Certificate",
		certificate_name,
		["name", "member", "issue_date", "expiry_date", "course"],
		as_dict=True,
	)

	if context.certificate.course != course_name:
		redirect_to_course_list()

	context.course = dontmanage.db.get_value(
		"LMS Course", course_name, ["title", "name", "image"], as_dict=True
	)
	context.instructors = (", ").join([x.full_name for x in get_instructors(course_name)])
	context.member = dontmanage.db.get_value(
		"User", context.certificate.member, ["full_name"], as_dict=True
	)

	context.logo = dontmanage.db.get_single_value("Website Settings", "banner_image")
	template_name = dontmanage.db.get_single_value(
		"LMS Settings", "custom_certificate_template"
	)
	context.custom_certificate_template = dontmanage.db.get_value(
		"Web Template", template_name, "template"
	)
	context.custom_template = render_template(context.custom_certificate_template, context)


def redirect_to_course_list():
	dontmanage.local.flags.redirect_location = "/courses"
	raise dontmanage.Redirect
