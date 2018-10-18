from odoo import api, fields, models

class ProductionFTQ(models.Model):
    _name = "production.ftq"

    @api.model
    def ftq_list(self):
        self.create(dict(name='demo.webkul.com'))