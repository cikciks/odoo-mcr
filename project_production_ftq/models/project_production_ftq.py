from odoo import api, fields, models

class ProductionFTQ(models.Model):
    _name = "production.ftq"

    parameter = fields.Char(required=False, string="Parameter")