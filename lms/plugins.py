"""
The plugins module provides various plugins to change the default
behaviour some parts of the lms app.

A site specify what plugins to use using appropriate entries in the dontmanage
hooks, written in the `hooks.py`.

This module exposes two plugins: ProfileTab and PageExtension.

The ProfileTab is used to specify any additional tabs to be displayed
on the profile page of the user.

The PageExtension is used to load additinal stylesheets and scripts to
be loaded in a webpage.
"""

import dontmanage


class PageExtension:
	"""PageExtension is a plugin to inject custom styles and scripts
	into a web page.

	The subclasses should overwrite the `render_header()` and
	`render_footer()` methods to inject whatever styles/scripts into
	the webpage.
	"""

	def __init__(self):
		self.context = dontmanage._dict()

	def set_context(self, context):
		self.context = context

	def render_header(self):
		"""Returns the HTML snippet to be included in the head section
		of the web page.

		Typically used to include the stylesheets and javascripts to be
		included in the <head> of the webpage.
		"""
		return ""

	def render_footer(self):
		"""Returns the HTML snippet to be included in the body tag at
		the end of web page.

		Typically used to include javascripts that need to be executed
		after the page is loaded.
		"""
		return ""


class ProfileTab:
	"""Base class for profile tabs.

	Every subclass of ProfileTab must implement two methods:
	    - get_title()
	    - render()
	"""

	def __init__(self, user):
		self.user = user

	def get_title(self):
		"""Returns the title of the tab.

		Every subclass must implement this.
		"""
		raise NotImplementedError()

	def render(self):
		"""Renders the contents of the tab as HTML.

		Every subclass must implement this.
		"""
		raise NotImplementedError()


class LiveCodeExtension(PageExtension):
	def render_header(self):
		livecode_url = dontmanage.get_value("LMS Settings", None, "livecode_url")
		context = {"livecode_url": livecode_url}
		return dontmanage.render_template("templates/livecode/extension_header.html", context)

	def render_footer(self):
		livecode_url = dontmanage.get_value("LMS Settings", None, "livecode_url")
		context = {"livecode_url": livecode_url}
		return dontmanage.render_template("templates/livecode/extension_footer.html", context)


def set_mandatory_fields_for_profile():
	profile_form = dontmanage.get_doc("Web Form", "profile")
	profile_mandatory_fields = dontmanage.get_hooks("profile_mandatory_fields")
	for field in profile_form.web_form_fields:
		field.reqd = 0
		if field.fieldname in profile_mandatory_fields:
			field.reqd = 1

	profile_form.save()


def quiz_renderer(quiz_name):
	quiz = dontmanage.get_doc("LMS Quiz", quiz_name)

	context = {"quiz": quiz}

	no_of_attempts = dontmanage.db.count(
		"LMS Quiz Submission", {"owner": dontmanage.session.user, "quiz": quiz_name}
	)

	if quiz.max_attempts and no_of_attempts >= quiz.max_attempts:
		last_attempt_score = dontmanage.db.get_value(
			"LMS Quiz Submission", {"owner": dontmanage.session.user, "quiz": quiz_name}, ["score"]
		)

		context.update({"attempts_exceeded": True, "last_attempt_score": last_attempt_score})
	return dontmanage.render_template("templates/quiz.html", context)


def exercise_renderer(argument):
	exercise = dontmanage.get_doc("LMS Exercise", argument)
	context = dict(exercise=exercise)
	return dontmanage.render_template("templates/exercise.html", context)


def youtube_video_renderer(video_id):
	return f"""
    <iframe width="100%" height="400"
        src="https://www.youtube.com/embed/{video_id}"
        title="YouTube video player"
        frameborder="0"
        style="border-radius: var(--border-radius-lg)"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen>
    </iframe>
    """


def video_renderer(src):
	return f"<video controls width='100%'><source src={src} type='video/mp4'></video>"


def assignment_renderer(detail):
	supported_types = {
		"Document": ".doc,.docx,.xml,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document",
		"PDF": ".pdf",
		"Image": ".png, .jpg, .jpeg",
		"Video": "video/*",
	}
	question = detail.split("-")[0]
	file_type = detail.split("-")[1]
	accept = supported_types[file_type] if file_type else ""
	return dontmanage.render_template(
		"templates/assignment.html",
		{"question": question, "accept": accept, "file_type": file_type},
	)


def show_custom_signup():
	if dontmanage.db.get_single_value(
		"LMS Settings", "terms_of_use"
	) or dontmanage.db.get_single_value("LMS Settings", "privacy_policy"):
		return "lms/templates/signup-form.html"
	return "dontmanage/templates/signup.html"
