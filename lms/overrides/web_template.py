import json

import dontmanage
from dontmanage.website.doctype.web_template.web_template import WebTemplate

from lms.widgets import Widgets


class CustomWebTemplate(WebTemplate):
	def render(self, values=None):
		if not values:
			values = {}
		values = dontmanage.parse_json(values)
		values.update({"values": values})
		values.update({"widgets": Widgets()})
		template = self.get_template(self.standard)
		return dontmanage.render_template(template, values)
