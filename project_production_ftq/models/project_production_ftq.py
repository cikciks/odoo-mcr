from odoo import api, fields, models

class ProductionFTQ(models.Model):
    _name = "project.production.ftq"

    name = fields.Char(required=False, string="Parameter")
    area = fields.Char(required=False, string="Area")
    state = fields.Char(required=False, string="State")
    note = fields.Char(required=False, string="Note")
    project_id = fields.Many2one("project.project", related='task_id.project_id', store=True)
    user_id = fields.Many2one('res.users', 'Assigned to', required=True)
    task_id = fields.Many2one('project.task', 'Task', ondelete='cascade', required=True, index="1")


class Task(models.Model):
    _inherit = "project.task"
    ftq_ids = fields.One2many('project.production.ftq', 'task_id', 'FTQ')
    default_user = fields.Many2one('res.users', compute='_compute_default_user')

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
