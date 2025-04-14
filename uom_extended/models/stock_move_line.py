from odoo import models, fields, api
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = 'stock.move.line'

    ref = fields.Char(string='Lote Fabricación')
    fecha_de_fabricacion = fields.Date(string="Fecha de fabricacion")
    metro_lineal_original = fields.Float(string="Metro Lineal Original")


    # Metodo re-definido para que se creen los valores nuevos en el lote
    def _prepare_new_lot_vals(self):
        self.ensure_one()
        return {
            'name': self.lot_name,
            'product_id': self.product_id.id,
            'company_id': self.company_id.id,
            'ref':self.ref,
            'fecha_de_fabricacion':self.fecha_de_fabricacion,
            'metro_lineal_original':self.metro_lineal_original,
        }
    
    @api.model
    def create(self, vals):
        res = super(StockMove, self).create(vals)
        # If the move line has a lot_id, update the lot with the new fields
        if res.lot_id:
            lot_vals = {
                'ref': res.lot_id.ref,
                'fecha_de_fabricacion': res.lot_id.fecha_de_fabricacion,
                'metro_lineal_original': res.lot_id.metro_lineal_original,
            }
            res.write(lot_vals)
        return res