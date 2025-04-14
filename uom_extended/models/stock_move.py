from odoo import models, fields, api
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = 'stock.move'


    millares = fields.Float(string='Millar(es)', compute='_compute_millares', store=False)
    millares_visible = fields.Boolean(string="Field Millar(es) invisible", compute="_compute_millares_visible", store=False)

    @api.depends('product_uom_qty','product_id')
    def _compute_millares(self):
        for record in self:
            millares = 0.0
            if record.product_id.product_cosal == 'hoja':
                for uom in record.product_id.secondary_uom_ids:
                    if uom:
                        millares = uom.factor_inv/ record.product_uom_qty if  uom.factor_inv and record.product_uom_qty else 0.0
                        break
            else:
                millares = None
            record.millares = millares

    @api.depends('product_id')
    def _compute_millares_visible(self):
        for record in self:
            millares_visible = False
            if record.product_id.product_cosal == 'hoja':
                millares_visible= True
            else:
                millares_visible= False
            record.millares_visible = millares_visible
            
    # @api.onchange('lot_id')
    # def _onchange_lot_id(self):
    #     if self.lot_id:
    #         self.ref = self.lot_id.ref
    #         self.fecha_de_fabricacion = self.lot_id.fecha_de_fabricacion
    #         self.metro_lineal_original = self.lot_id.metro_lineal_original