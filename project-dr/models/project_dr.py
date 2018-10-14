from odoo import models, fields, api
from odoo.tools import html_escape as escape
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _



RESULT_TYPES = {'material': 'Incoming Analysis Results',
                'production': 'Online Testing Analysis Results',
                'laboratory': 'Finished Product Analysys Result',
                'enviroment': 'Pathogen & Hygiene Monitoring Result'}


class ProjectTaskSubtask(models.Model):
    _inherit = "project.task.subtask"
    result_type = fields.Selection([(k, v) for k, v in list(RESULT_TYPES.items())],
                             'Analysis Type', required=True, copy=False, default='material')
    reference = fields.Char(required=False, string="Reference")
    specification = fields.Char(required=False, string="Specification")
    result = fields.Char(required=False, string="Result")
    remark = fields.Char(required=False, string="Remark")
