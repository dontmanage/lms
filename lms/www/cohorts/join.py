import dontmanage

from . import utils


def get_context(context):
	context.no_cache = 1

	course = utils.get_course(dontmanage.form_dict["course"])
	cohort = course and utils.get_cohort(course, dontmanage.form_dict["cohort"])
	subgroup = cohort and utils.get_subgroup(cohort, dontmanage.form_dict["subgroup"])
	if not subgroup:
		context.template = "www/404.html"
		return

	invite_code = dontmanage.form_dict["invite_code"]
	if subgroup.invite_code != invite_code:
		context.template = "www/404.html"
		return

	utils.add_nav(context, "All Courses", "/courses")
	utils.add_nav(context, course.title, "/courses/" + course.name)

	context.course = course
	context.cohort = cohort
	context.subgroup = subgroup
