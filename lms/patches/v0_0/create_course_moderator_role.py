from venv import create

import dontmanage

from lms.install import create_moderator_role


def execute():
	create_moderator_role()
