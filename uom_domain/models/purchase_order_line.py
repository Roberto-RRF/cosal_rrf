from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    allowed_uom_ids = fields.Many2many(
        'uom.uom',
        compute='_compute_allowed_uom_ids',
        string='Allowed UoMs',
        store=False,
    )

    @api.depends('product_id', 'product_id.uom_id', 'product_id.secondary_uom_ids')
    def _compute_allowed_uom_ids(self):
        for line in self:
            uoms = self.env['uom.uom']
            if line.product_id:
                # Add main UoM and any secondary UoMs
                uoms |= line.product_id.uom_id
                uoms |= line.product_id.secondary_uom_ids
            line.allowed_uom_ids = uoms
