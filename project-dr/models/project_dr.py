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
    name = fields.Many2one('dr.parameter', string='Parameter')
    result_type = fields.Selection([(k, v) for k, v in list(RESULT_TYPES.items())],
                             'Analysis Type', required=True, copy=False, default='material')
    reference = fields.Char(required=False, string="Reference")
    specification = fields.Char(required=False, string="Specification")
    result = fields.Char(required=False, string="Result")
    remark = fields.Char(required=False, string="Remark")

    @api.multi
    def write(self, vals):
        old_names = dict(list(zip(self.mapped('id'), self.mapped('name'))))
        result = super(ProjectTaskSubtask, self).write(vals)
        for r in self:
            if vals.get('state'):
                r.task_id.send_subtask_email(r.name.id, r.state, r.reviewer_id.id, r.user_id.id)
                if self.env.user != r.reviewer_id and self.env.user != r.user_id:
                    raise UserError(_('Only users related to that subtask can change state.'))
            if vals.get('name'):
                r.task_id.send_subtask_email(r.name.id, r.state, r.reviewer_id.id, r.user_id.id, old_name=old_names[r.id])
                if self.env.user != r.reviewer_id and self.env.user != r.user_id:
                    raise UserError(_('Only users related to that subtask can change state.'))
            if vals.get('user_id'):
                r.task_id.send_subtask_email(r.name.id, r.state, r.reviewer_id.id, r.user_id.id)
        return result

    @api.model
    def create(self, vals):
        result = super(ProjectTaskSubtask, self).create(vals)
        vals = self._add_missing_default_values(vals)
        task = self.env['project.task'].browse(vals.get('task_id'))
        task.send_subtask_email(vals['name'], vals['state'], vals['reviewer_id'], vals['user_id'])
        return result

class DRParameter(models.Model):
    _name = 'dr.parameter'
    _description = 'Parameter for Document Release'

    name = fields.Char(string='Name', required=True)
    parameter_type = fields.Many2one('dr.parameter_type', 'Parameter Type')


class DRParameterType(models.Model):
    _name = 'dr.parameter_type'
    _description = 'Parameter Type'

    name = fields.Char(string='Name', required=True)


