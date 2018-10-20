from odoo import models, fields, api
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


PRODUCT_TYPES = {'cnc02': 'Anchor Cheddar Potong 2kg',
                 'cnc03': 'Anchor Shredded Cheese Pale 1kg',
                 'cnc09': 'NZ Mozarella Potong 2kg',
                 'cnc11': 'NZ Parmesan Block 0.8kg',
                 'cnc12': 'Shredded Parmesan 1kg',
                 'cnc13': 'Grated Parmesan 1kg'}


class ProjectTask(models.Model):
    _inherit = 'project.task'
    product_type = fields.Selection([(k, v) for k, v in list(PRODUCT_TYPES.items())],
                                    'Product', required=True, copy=False, default='cnc02')
    shelf_life = fields.Integer(required=False, string="Shelf Life (days)")
    lot = fields.Char(required=False, string="Lot Number")
    weight_pack = fields.Float(required=False, string="Weight per Pack (kg)")
    weight_box = fields.Float(required=False, string="Weight per Box (kg)")
    qty_in_box = fields.Integer(required=False, string="Quantity in Box")
    qty_in_pack = fields.Integer(required=False, string="Quantity in Pack")
    qty_sample = fields.Integer(required=False, string="Sample Qty (pack)")
    weight_sample = fields.Float(required=False, string="Sample Weight (kg)")
    weight_rm = fields.Float(required=False, string="Raw Material (kg)")
    date_prod = fields.Date(required=True, string="Production Date", default=fields.Date.today)
    date_rel_deadline = fields.Date(required=False, string="Release Deadline")
    date_release = fields.Date(required=False, string="Release Date", compute='_compute_release')
    date_bb = fields.Date(required=False, string="Best Before Date",compute='_compute_bb')
    prod_status = fields.Char(required=False, string="Status")
    date_sample1 = fields.Datetime(required=False, string="Ship to MR", default=fields.Datetime.now)
    date_sample2 = fields.Datetime(required=False, string="Taken by Courier", default=fields.Datetime.now)
    date_sample3 = fields.Datetime(required=False, string="Received by Lab",  default=fields.Datetime.now)
    shipment_duration = fields.Float(digits=(6, 2), help="Shipment Duration in days")

    @api.onchange('date_prod','shelf_life')
    def _compute_bb(self):
        expiry_date = (datetime.strptime(self.date_prod, '%Y-%m-%d') + relativedelta(days=+ self.shelf_life))
        self.date_bb = expiry_date

    @api.onchange('date_prod')
    def _compute_release(self):
        release_date = (datetime.strptime(self.date_prod, '%Y-%m-%d') + relativedelta(days=+ 10))
        self.date_rel_deadline = release_date


    @api.onchange('date_sample1', 'date_sample3')
    def _compute_ship_duration(self):
        if self.date_sample1 and self.date_sample3:
            sample1_dt = fields.Datetime.from_string(self.date_sample1)
            sample2_dt = fields.Datetime.from_string(self.date_sample3)
            difference = relativedelta(sample1_dt, sample2_dt)
            days = difference.days
            hours = difference.hours
            minutes = difference.minutes
            seconds = 0