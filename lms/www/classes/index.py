import dontmanage
from dontmanage.utils import getdate


def get_context(context):
	context.no_cache = 1

	context.classes = dontmanage.get_all(
		"LMS Class",
		{"end_date": [">=", getdate()]},
		["name", "title", "start_date", "end_date"],
	)
