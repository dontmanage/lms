# Copyright (c) 2022, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document
from dontmanage import _
from dontmanage.utils import cint, format_date, format_datetime
import requests
import base64
import json


class LMSClass(Document):
	def validate(self):
		self.validate_duplicate_students()
		self.validate_membership()

	def validate_duplicate_students(self):
		students = [row.student for row in self.students]
		duplicates = {student for student in students if students.count(student) > 1}
		if len(duplicates):
			dontmanage.throw(
				_("Student {0} has already been added to this class.").format(
					dontmanage.bold(next(iter(duplicates)))
				)
			)

	def validate_membership(self):
		for course in self.courses:
			for student in self.students:
				filters = {
					"doctype": "LMS Batch Membership",
					"member": student.student,
					"course": course.course,
				}
				if not dontmanage.db.exists(filters):
					dontmanage.get_doc(filters).save()


@dontmanage.whitelist()
def add_student(email, class_name):
	if not dontmanage.db.exists("User", email):
		dontmanage.throw(_("There is no such user. Please create a user with this Email ID."))

	filters = {
		"student": email,
		"parent": class_name,
		"parenttype": "LMS Class",
		"parentfield": "students",
	}
	if dontmanage.db.exists("Class Student", filters):
		dontmanage.throw(
			_("Student {0} has already been added to this class.").format(dontmanage.bold(email))
		)

	dontmanage.get_doc(
		{
			"doctype": "Class Student",
			"student": email,
			"student_name": dontmanage.db.get_value("User", email, "full_name"),
			"parent": class_name,
			"parenttype": "LMS Class",
			"parentfield": "students",
		}
	).save()
	return True


@dontmanage.whitelist()
def remove_student(student, class_name):
	dontmanage.db.delete("Class Student", {"student": student, "parent": class_name})
	return True


@dontmanage.whitelist()
def update_course(class_name, course, value):
	if cint(value):
		doc = dontmanage.get_doc(
			{
				"doctype": "Class Course",
				"parent": class_name,
				"course": course,
				"parenttype": "LMS Class",
				"parentfield": "courses",
			}
		)
		doc.save()
	else:
		dontmanage.db.delete("Class Course", {"parent": class_name, "course": course})
	return True


@dontmanage.whitelist()
def create_live_class(
	class_name, title, duration, date, time, timezone, auto_recording, description=None
):
	date = format_date(date, "yyyy-mm-dd", True)

	payload = {
		"topic": title,
		"start_time": format_datetime(f"{date} {time}", "yyyy-MM-ddTHH:mm:ssZ"),
		"duration": duration,
		"agenda": description,
		"private_meeting": True,
		"auto_recording": "none"
		if auto_recording == "No Recording"
		else auto_recording.lower(),
		"timezone": timezone,
	}
	headers = {
		"Authorization": "Bearer " + authenticate(),
		"content-type": "application/json",
	}
	response = requests.post(
		"https://api.zoom.us/v2/users/me/meetings", headers=headers, data=json.dumps(payload)
	)

	if response.status_code == 201:
		data = json.loads(response.text)
		payload.update(
			{
				"doctype": "LMS Live Class",
				"start_url": data.get("start_url"),
				"join_url": data.get("join_url"),
				"title": title,
				"host": dontmanage.session.user,
				"date": date,
				"time": time,
				"class_name": class_name,
				"password": data.get("password"),
				"description": description,
				"auto_recording": auto_recording,
			}
		)
		class_details = dontmanage.get_doc(payload)
		class_details.save()
		return class_details


def authenticate():
	zoom = dontmanage.get_single("Zoom Settings")
	if not zoom.enable:
		dontmanage.throw(_("Please enable Zoom Settings to use this feature."))

	authenticate_url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={zoom.account_id}"

	headers = {
		"Authorization": "Basic "
		+ base64.b64encode(
			bytes(
				zoom.client_id
				+ ":"
				+ zoom.get_password(fieldname="client_secret", raise_exception=False),
				encoding="utf8",
			)
		).decode()
	}
	response = requests.request("POST", authenticate_url, headers=headers)
	return response.json()["access_token"]
