# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class CohortWebPage(Document):
	def get_template_html(self):
		return dontmanage.get_doc("Web Template", self.template).template
