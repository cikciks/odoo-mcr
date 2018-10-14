from odoo import models, fields, api
from odoo.tools import html_escape as escape
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _

class ProjectTaskSubtask(models.Model):
    _inherit = "project.task.subtask"
    reference = fields.Char(required=True, string="Reference")
    specification = fields.Char(required=True, string="Specification")
    result = fields.Char(required=True, string="Result")
    remark = fields.Char(required=True, string="Remark")
