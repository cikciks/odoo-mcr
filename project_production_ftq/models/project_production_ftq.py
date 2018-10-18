from odoo import api, fields, models

class ProductionFTQ(models.Model):
    _name = "production.ftq"
    @api.model
    def oe_method_without_params(self):
        self.create(dict(name='demo.webkul.com'))