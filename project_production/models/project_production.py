from odoo import models, fields, api
from odoo.tools import html_escape as escape
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _



PRODUCT_TYPES = {'cnc02': 'Anchor Cheddar Potong 2kg',
                'cnc03': 'Anchor Shredded Cheese Pale 1kg',
                'cnc09': 'NZ Mozarella Potong 2kg',
                'cnc11': 'NZ Parmesan Block 0.8kg',
                'cnc12': 'Shredded Parmesan 1kg',
                'cnc13': 'Grated Parmesan 1kg'}


class ProjectProduction(models.Model):
    _inherit = "project.task"
    product_type = fields.Selection([(k, v) for k, v in list(PRODUCT_TYPES.items())],
                             'Product', required=True, copy=False, default='cnc02')
    lot = fields.Char(required=False, string="Lot Number")
    weight_pack = fields.Char(required=False, string="Weight Pack")
    weight_box = fields.Char(required=False, string="Weight Box")
    quantity = fields.Char(required=False, string="Quantity")
