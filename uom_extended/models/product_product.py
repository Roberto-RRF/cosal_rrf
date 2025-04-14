from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    millares_rollos_a_la_mano = fields.Float(string='Millar(es)/Rollos on hand', compute='_compute_millares_rollos_on_hand', store=False)
    millares_rollos_disponible = fields.Float(string='Millar(es)/Rollos Disponibles', compute='_compute_millares_rollos_disponible', store=False)

    @api.depends('qty_available')
    def _compute_millares_rollos_on_hand(self):
        for record in self:
            try:
                if record.product_cosal == 'hoja' and record.secondary_uom_ids:
                    for uom in record.secondary_uom_ids:
                        if uom:
                            record.millares_rollos_a_la_mano = record.qty_available / uom.factor_inv
                            break
                        else:
                            record.millares_rollos_a_la_mano = None
                elif record.product_cosal == 'rollo' and record.secondary_uom_ids:
                    res = self.env['stock.lot'].search([('product_id','=',record.id)])
                    record.millares_rollos_a_la_mano = len(res)
                else:
                    record.millares_rollos_a_la_mano = None
            except ValueError:
                record.millares_rollos_a_la_mano = None

    @api.depends('free_qty')
    def _compute_millares_rollos_disponible(self):
        for record in self:
            try: 
                if record.product_cosal == 'hoja' and record.secondary_uom_ids:
                    for uom in record.secondary_uom_ids:
                        if uom:
                            record.millares_rollos_disponible = record.free_qty / uom.factor_inv
                            break
                        else:
                            record.millares_rollos_disponible = None
                elif record.product_cosal == 'rollo':
                    res = self.env['stock.lot'].search([('product_id','=',record.id),('product_qty','>',0)])
                    record.millares_rollos_disponible = len(res)
                else:
                    record.millares_rollos_disponible = None
            except ValueError:
                record.millares_rollos_disponible = 0.0
        
