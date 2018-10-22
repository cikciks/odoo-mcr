from odoo import api, fields, models

LOC_TYPES = {'mr': 'MR', 'mcr': 'MCR'}


class ProductionFTQ(models.Model):
    _name = "project.production.ftq"

    # name = fields.Char(required=False, string="Parameter")
    parameter = fields.Many2one('ftq.parameter', string='Parameter')
    check_point = fields.Many2one('ftq.checkpoint', compute='_compute_check_point', string='Check Point')
    state = fields.Char(required=False, string="State")
    note = fields.Char(required=False, string="Note")
    project_id = fields.Many2one("project.project", related='task_id.project_id', store=True)
    task_id = fields.Many2one('project.task', 'Task', ondelete='cascade', required=True, index="1")

    @api.multi
    def _compute_checkpoint(self):
        if self.check_point:
            record = self.env['ftq.checkpoint'].browse[self.parameter.checkpoint_ids]
        record.write('check_point': id)


class Task(models.Model):
    _inherit = "project.task"
    ftq_ids = fields.One2many('project.production.ftq', 'task_id', 'FTQ')
    default_user = fields.Many2one('res.users', compute='_compute_default_user')
    score = fields.Char(required=False, string="Score")

    @api.multi
    def _compute_default_user(self):
        for record in self:
            if self.env.user != record.user_id and self.env.user != record.create_uid:
                record.default_user = record.user_id
            else:
                if self.env.user != record.user_id:
                    record.default_user = record.user_id
                elif self.env.user != record.create_uid:
                    record.default_user = record.create_uid
                elif self.env.user == record.create_uid and self.env.user == record.user_id:
                    record.default_user = self.env.user

class FTQParameter(models.Model):
    _name = 'ftq.parameter'
    _description = 'Parameter for FTQ'

    name = fields.Char(string='Name', required=True)
    checkpoint_ids = fields.Many2one('ftq.checkpoint', 'Check Point Area')


class FTQCheckPoint(models.Model):
    _name = 'ftq.checkpoint'
    _description = 'Check Point for FTQ'

    name = fields.Char(string='Name', required=True)
    location = fields.Selection([(k, v) for k, v in list(LOC_TYPES.items())],
                     'Location', required=True, copy=False, default='mcr')
