import dontmanage

from lms.lms.utils import get_lesson_index
from lms.page_renderers import get_profile_url_prefix


def get_context(context):
	context.no_cache = 1

	try:
		username = dontmanage.form_dict["username"]
	except KeyError:
		username = dontmanage.db.get_value("User", dontmanage.session.user, ["username"])
		if username:
			dontmanage.local.flags.redirect_location = get_profile_url_prefix() + username
			raise dontmanage.Redirect

	try:
		context.member = dontmanage.get_doc("User", {"username": username})
	except Exception:
		context.template = "www/404.html"
		return

	context.profile_tabs = get_profile_tabs(context.member)
	context.notifications = get_notifications()


def get_profile_tabs(user):
	"""Returns the enabled ProfileTab objects.

	Each ProfileTab is rendered as a tab on the profile page and the
	they are specified as profile_tabs hook.
	"""
	tabs = dontmanage.get_hooks("profile_tabs") or []
	return [dontmanage.get_attr(tab)(user) for tab in tabs]


def get_notifications():
	notifications = dontmanage.get_all(
		"Notification Log",
		{"document_type": "Course Lesson", "for_user": dontmanage.session.user},
		["subject", "creation", "from_user", "document_name"],
	)

	for notification in notifications:
		course = dontmanage.db.get_value("Course Lesson", notification.document_name, "course")
		notification.url = (
			f"/courses/{course}/learn/{get_lesson_index(notification.document_name)}"
		)

	return notifications
