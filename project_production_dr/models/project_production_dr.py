from odoo import models, fields, api
from odoo.tools import html_escape as escape
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


SUBTASK_STATES = {'done': 'Done',
                  'todo': 'TODO',
                  'waiting': 'Waiting',
                  'cancelled': 'Cancelled'}

RESULT_TYPES = {'material': 'Incoming Analysis Results',
                'production': 'Online Testing Analysis Results',
                'laboratory': 'Finished Product Analysis Result',
                'enviroment': 'Pathogen & Hygiene Monitoring Result'}


class ProductionDR(models.Model):
    _name = "project.production.dr"
    _inherit = ['mail.activity.mixin']
    state = fields.Selection([(k, v) for k, v in list(SUBTASK_STATES.items())],
                             'Status', required=True, copy=False, default='todo')
    # name = fields.Char(required=True, string="Description")
    name = fields.Many2one('dr.parameter', string='Parameter')
    result_type = fields.Many2one('dr.parameter_type', compute='_compute_parameter_type', string='Parameter Type')
    # result_type = fields.Selection([(k, v) for k, v in list(RESULT_TYPES.items())],
    #                         'Analysis Type', required=True, copy=False, default='material')
    reference = fields.Char(required=False, string="Reference")
    # specification = fields.Many2one('dr.parameter', compute='_compute_specification', string='Specification')
    specification = fields.Char(required=False, compute='_compute_specification', string="Specification")
    result = fields.Char(required=False, string="Result")
    remark = fields.Char(required=False, string="Remark")
    reviewer_id = fields.Many2one('res.users', 'Created by', readonly=True, default=lambda self: self.env.user)
    project_id = fields.Many2one("project.project", related='task_id.project_id', store=True)
    user_id = fields.Many2one('res.users', 'Assigned to', required=True)
    task_id = fields.Many2one('project.task', 'Task', ondelete='cascade', required=True, index="1")
    task_state = fields.Char(string='Task state', related='task_id.stage_id.name', readonly=True)
    hide_button = fields.Boolean(compute='_compute_hide_button')
    recolor = fields.Boolean(compute='_compute_recolor')
    deadline = fields.Date(string="Deadline")

    @api.multi
    def _compute_recolor(self):
        for record in self:
            if self.env.user == record.user_id and record.state == 'todo':
                record.recolor = True

    @api.multi
    def _compute_hide_button(self):
        for record in self:
            if self.env.user not in [record.reviewer_id, record.user_id]:
                record.hide_button = True

    @api.multi
    def _compute_reviewer_id(self):
        for record in self:
            record.reviewer_id = record.create_uid

    @api.model
    def _needaction_domain_get(self):
        if self._needaction:
            return [('state', '=', 'todo'), ('user_id', '=', self.env.uid)]
        return []

    @api.multi
    def write(self, vals):
        old_names = dict(list(zip(self.mapped('id'), self.mapped('name'))))
        result = super(ProductionDR, self).write(vals)
        for r in self:
            if vals.get('state'):
                r.task_id.send_subtask_email(r.name.name, r.state, r.reviewer_id.id, r.user_id.id)
                if self.env.user != r.reviewer_id and self.env.user != r.user_id:
                    raise UserError(_('Only users related to that subtask can change state.'))
            if vals.get('name'):
                r.task_id.send_subtask_email(r.name.name, r.state, r.reviewer_id.id, r.user_id.id, old_name=old_names[r.id])
                if self.env.user != r.reviewer_id and self.env.user != r.user_id:
                    raise UserError(_('Only users related to that subtask can change state.'))
            if vals.get('user_id'):
                r.task_id.send_subtask_email(r.name.name, r.state, r.reviewer_id.id, r.user_id.id)
        return result

    @api.model
    def create(self, vals):
        result = super(ProductionDR, self).create(vals)
        vals = self._add_missing_default_values(vals)
        task = self.env['project.task'].browse(vals.get('task_id'))
        task.send_subtask_email(vals['name'], vals['state'], vals['reviewer_id'], vals['user_id'])
        return result

    @api.multi
    def change_state_done(self):
        for record in self:
            record.state = 'done'

    @api.multi
    def change_state_todo(self):
        for record in self:
            record.state = 'todo'

    @api.multi
    def change_state_cancelled(self):
        for record in self:
            record.state = 'cancelled'

    @api.multi
    def change_state_waiting(self):
        for record in self:
            record.state = 'waiting'

    @api.one
    @api.depends('name')
    def _compute_parameter_type(self):
        self.result_type = self.name.parameter_type

    @api.one
    @api.depends('name')
    def _compute_specification(self):
        self.specification = self.name.specification

    @api.one
    def _compute_deadline(self):
        deadline = datetime.now() + relativedelta(days=+ 5)
        self.deadline = deadline


class Task(models.Model):
    _inherit = "project.task"
    subtask_ids = fields.One2many('project.production.dr', 'task_id', 'Subtask')
    kanban_subtasks = fields.Text(compute='_compute_kanban_subtasks')
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

    @api.multi
    def _compute_kanban_subtasks(self):
        for record in self:
            result_string1 = ''
            result_string2 = ''
            result_string3 = ''
            for subtask in record.subtask_ids:
                bounding_length = 25
                tmp_list = (subtask.name.name).split()
                for index in range(len(tmp_list)):
                    if len(tmp_list[index]) > bounding_length:
                        tmp_list[index] = tmp_list[index][:bounding_length] + '...'
                tmp_subtask_name = " ".join(tmp_list)
                if subtask.state == 'todo' and record.env.user == subtask.user_id and record.env.user == subtask.reviewer_id:
                    tmp_string3 = escape(': {0}'.format(tmp_subtask_name))
                    result_string3 += '<li><b>TODO</b>{}</li>'.format(tmp_string3)
                elif subtask.state == 'todo' and record.env.user == subtask.user_id:
                    tmp_string1_1 = escape('{0}'.format(subtask.reviewer_id.name))
                    tmp_string1_2 = escape('{0}'.format(tmp_subtask_name))
                    result_string1 += '<li><b>TODO</b> from <em>{0}</em>: {1}</li>'.format(tmp_string1_1, tmp_string1_2)
                elif subtask.state == 'todo' and record.env.user == subtask.reviewer_id:
                    tmp_string2_1 = escape('{0}'.format(subtask.user_id.name))
                    tmp_string2_2 = escape('{0}'.format(tmp_subtask_name))
                    result_string2 += '<li>TODO for <em>{0}</em>: {1}</li>'.format(tmp_string2_1, tmp_string2_2)
            record.kanban_subtasks = '<ul>' + result_string1 + result_string3 + result_string2 + '</ul>'

    @api.multi
    def send_subtask_email(self, subtask_name, subtask_state, subtask_reviewer_id, subtask_user_id, old_name=None):
        for r in self:
            body = ''
            reviewer = self.env["res.users"].browse(subtask_reviewer_id)
            user = self.env["res.users"].browse(subtask_user_id)
            state = SUBTASK_STATES[subtask_state]
            if subtask_state == 'done':
                state = '<span style="color:#080">' + state + '</span>'
            if subtask_state == 'todo':
                state = '<span style="color:#A00">' + state + '</span>'
            if subtask_state == 'cancelled':
                state = '<span style="color:#777">' + state + '</span>'
            if subtask_state == 'waiting':
                state = '<span style="color:#b818ce">' + state + '</span>'
            partner_ids = []
            subtype = 'project_production_dr.subtasks_subtype'
            if user == self.env.user and reviewer == self.env.user:
                body = '<p>' + '<strong>' + state + '</strong>: ' + escape(subtask_name)
                subtype = False
            elif self.env.user == reviewer:
                body = '<p>' + escape(user.name) + ', <br><strong>' + state + '</strong>: ' + escape(subtask_name)
                partner_ids = [user.partner_id.id]
            elif self.env.user == user:
                body = '<p>' + escape(reviewer.name) + ', <em style="color:#999">I updated checklist item assigned to me:</em> <br><strong>' + state + '</strong>: ' + escape(subtask_name)
                partner_ids = [reviewer.partner_id.id]
            else:
                body = '<p>' + escape(user.name) + ', ' + escape(reviewer.name) + ', <em style="color:#999">I updated checklist item, now its assigned to ' + escape(user.name) + ': </em> <br><strong>' + state + '</strong>: ' + escape(subtask_name)
                partner_ids = [user.partner_id.id, reviewer.partner_id.id]
            if old_name:
                body = body + '<br><em style="color:#999">Updated from</em><br><strong>' + state + '</strong>: ' + escape(old_name) + '</p>'
            else:
                body = body + '</p>'
            r.message_post(message_type='comment',
                           subtype=subtype,
                           body=body,
                           partner_ids=partner_ids)



class DRParameter(models.Model):
    _name = 'dr.parameter'
    _description = 'Parameter for Document Release'

    name = fields.Char(string='Name', required=True)
    parameter_type = fields.Many2one('dr.parameter_type', 'Parameter Type')
    specification = fields.Char(string='Specification', required=False)


class DRParameterType(models.Model):
    _name = 'dr.parameter_type'
    _description = 'Parameter Type'

    name = fields.Char(string='Name', required=True)
