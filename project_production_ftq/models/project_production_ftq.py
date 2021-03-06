from odoo import api, fields, models

LOC_TYPES = {'mr': 'MR', 'mcr': 'MCR'}


class ProductionFTQ(models.Model):
    _name = "project.production.ftq"

    # name = fields.Char(required=False, string="Parameter")
    parameter = fields.Many2one('ftq.parameter', string='Parameter')
    check_point = fields.Many2one('ftq.checkpoint', compute='_compute_check_point', string='Check Point')
    mark_point = fields.Boolean(required=False, string="Point")
    note = fields.Char(required=False, string="Note")
    project_id = fields.Many2one("project.project", related='task_id.project_id', store=True)
    task_id = fields.Many2one('project.task', 'Task', ondelete='cascade', required=True, index="1")

    @api.one
    @api.depends('parameter')
    def _compute_check_point(self):
        self.check_point = self.parameter.checkpoint_ids


class Task(models.Model):
    _inherit = "project.task"
    ftq_ids = fields.One2many('project.production.ftq', 'task_id', 'FTQ')
    default_user = fields.Many2one('res.users', compute='_compute_default_user')
    total_parameter = fields.Integer(compute='_count_total_parameter')
    total_point = fields.Integer(compute='_count_total_point')
    # total_point = fields.Char(required=False, string="Note")
    score = fields.Float(compute='_compute_score', string='Score (%)')

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

    @api.one
    @api.depends('ftq_ids')
    def _count_total_parameter(self):
        task_id = self.id
        # self.total_parameter = self.ftq_ids.search_count([])
        # self.total_parameter = task_id
        self.total_parameter = self.ftq_ids.search_count([('task_id', '=', task_id)])

    @api.one
    @api.depends('ftq_ids')
    def _count_total_point(self):
        task_id = self.id
        # parameter = self.ftq_ids.search([('task_id', '=', task_id)])
        # parameter = self.ftq_ids.filtered(lambda r: r.task_id == task_id)
        # parameter = self.ftq_ids.search([('task_id', '=', task_id)])
        # self.total_point = parameter.search_count([('mark_point', '=', True)])
        # self.total_point = parameter
        self.total_point = self.ftq_ids.search_count([('task_id', '=', task_id), ('mark_point', '=', True)])

    @api.depends('total_parameter','total_point')
    def _compute_score(self):
        if self.total_parameter > 0:
            self.score = (self.total_point / self.total_parameter) * 100


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
