from odoo import models, fields, api
from odoo.tools import html_escape as escape
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _



RESULT_TYPES = {'material': 'Incoming Analysis Results',
                'production': 'Online Testing Analysis Results',
                'laboratory': 'Finished Product Analysis Result',
                'enviroment': 'Pathogen & Hygiene Monitoring Result'}


class ProjectTaskSubtask(models.Model):
    _inherit = "project.task.subtask"
    # name = fields.Many2one('dr.parameter', string='Parameter')
    result_type = fields.Selection([(k, v) for k, v in list(RESULT_TYPES.items())],
                             'Analysis Type', required=True, copy=False, default='material')
    reference = fields.Char(required=False, string="Reference")
    specification = fields.Char(required=False, string="Specification")
    result = fields.Char(required=False, string="Result")
    remark = fields.Char(required=False, string="Remark")


class DRParameter(models.Model):
    _name = 'dr.parameter'
    _description = 'Parameter for Document Release'

    name = fields.Char(string='Name', required=True)
    parameter_type = fields.Many2one('dr.parameter_type', 'Parameter Type')


class DRParameterType(models.Model):
    _name = 'dr.parameter_type'
    _description = 'Parameter Type'

    name = fields.Char(string='Name', required=True)


