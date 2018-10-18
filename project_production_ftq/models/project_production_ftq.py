from odoo import api, fields, models

class ProductionFTQ(models.Model):
    _name = "project.production.ftq"

    @api.depends('ftq.checkpoint')
    def checkpoint_list(self):
        """:return the value for the check point list"""
        for rec in self:
            total_len = self.env['ftq.checkpoint'].search_count([])
            checkpoint_list_len = len(rec.ftq.checkpoint)
            if total_len != 0:
                rec.checkpoint_list = (checkpoint_list_len*100) / total_len

    name = fields.Char(required=False, string="Parameter")
    check_point = fields.Char(required=False, string="Check Point")
    state = fields.Char(required=False, string="State")
    note = fields.Char(required=False, string="Note")
    project_id = fields.Many2one("project.project", related='task_id.project_id', store=True)
    task_id = fields.Many2one('project.task', 'Task', ondelete='cascade', required=True, index="1")


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

class FTQ.CheckPoint(models.Model):
    _name = 'ftq.checkpoint'
    _description = 'Check Point for FTQ'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
