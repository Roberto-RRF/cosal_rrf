from odoo import models, fields, api
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    cantidad_embalaje = fields.Float(string='Cantidad Embalaje')

    @api.model 
    def create(self, vals):
        origin = vals.get('origin')
        if origin:
            sale_order = self.env['sale.order'].search([('name', '=', origin)], limit=1)
            if sale_order:
                try:
                # Get all unique product_packaging_id values, ignoring empty ones
                    packaging_records = sale_order.order_line.mapped('product_packaging_id').filtered(lambda p: p.id)
                    unique_packaging_ids = list(set(packaging_records.ids))
                    vals['cantidad_embalaje'] = packaging_records[0].qty
                except Exception as e:
                    pass
                if len(unique_packaging_ids) == 1 and packaging_records:
                    # Case: All packaging IDs are the same
                    total_qty = sum(sale_order.order_line.mapped('product_uom_qty'))
                    packaging_name = packaging_records[0].display_name if packaging_records else ''
                    vals['tarimas'] = f"{int(total_qty)} {packaging_name}"
                    vals['tarimas_iguales'] = True
                else:
                    # Case: Different packaging IDs
                    total_qty = sum(sale_order.order_line.mapped('product_uom_qty'))
                    vals['tarimas'] = f"{int(total_qty)}"
                    vals['tarimas_iguales'] = False
                    detalles_list = []

                    # Compute the total quantity for each unique packaging
                    packaging_qty = {}
                    for line in sale_order.order_line:
                        packaging = line.product_packaging_id
                        if packaging:
                            if packaging in packaging_qty:
                                packaging_qty[packaging] += line.product_uom_qty
                            else:
                                packaging_qty[packaging] = line.product_uom_qty

                    # Create a detail for each packaging with its calculated quantity
                    for packaging, qty in packaging_qty.items():
                        detalles_list.append((0, 0, {
                            'name': f"{int(qty)} x {packaging.display_name}"
                        }))

                    vals['detalles_tarimas'] = detalles_list

        return super(MrpProduction, self).create(vals)
    
    @api.constrains('state')
    def _check_state_and_update_product_qty(self):
        for rec in self:
            # raise UserError(rec.cantidad_embalaje)
            if rec.state == 'confirmed':
                rec.qty_producing = rec.cantidad_embalaje
                
