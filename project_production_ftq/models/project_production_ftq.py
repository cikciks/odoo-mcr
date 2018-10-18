from odoo import api, fields, models

class ProductionFTQ(models.Model):
    _name = "project.production.ftq"

    name = fields.Char(required=False, string="Parameter")
    area = fields.Char(required=False, string="Area")
    state = fields.Char(required=False, string="State")
    note = fields.Char(required=False, string="Note")
