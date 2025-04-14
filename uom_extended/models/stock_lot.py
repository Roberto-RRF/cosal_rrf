from odoo import models, fields, api

class StockLot(models.Model):
    _inherit = 'stock.lot'

    metro_lineal_original = fields.Float(string="Metro Lineal Original")
    factor = fields.Float(string="Factor", compute="_compute_factor", store=False)
    metro_lineal_remanente = fields.Float(string="Metro Lineal Remanente", compute="_compute_metro_lineal_remanente", store=False)
    fecha_de_fabricacion = fields.Date(string="Fecha de fabricacion")
    proveedor_id = fields.Many2one(
        comodel_name='res.partner', 
        string='Proveedor', 
        compute='_compute_proveedor_id',
    )
    es_rollo = fields.Boolean(string="Es Rollo", compute="_compute_es_rollo")


    # Campo redefinido para cambiar la etiqueta
    ref = fields.Char(string='Lote Fabricación', help="Internal reference number in case it differs from the manufacturer's lot/serial number")

    @api.depends('product_qty','metro_lineal_original')
    def _compute_factor(self):
        for rec in self:
            if rec.factor:
                #print("Adentro de if: "+str(rec.factor))
                rec.factor = rec.factor
                break
            else: 
                #print("Adentro de else factor: "+str(rec.metro_lineal_original/rec.product_qty))
                rec.factor = rec.metro_lineal_original/rec.product_qty if rec.metro_lineal_original else rec.product_qty
                break
    
    @api.depends('product_qty','factor')
    def _compute_metro_lineal_remanente(self):
        for rec in self:
            rec.metro_lineal_remanente = rec.factor * rec.product_qty
            break

    def _compute_proveedor_id(self):
        for rec in self:
            if rec.purchase_order_ids:
                for purchase in rec.purchase_order_ids:
                    rec.proveedor_id = purchase.partner_id
                    break
            else:
                rec.proveedor_id = ""

    def _compute_es_rollo(self):
        for rec in self:
            if rec.product_id.product_cosal == 'rollo':
                rec.es_rollo = True
            else:
                rec.es_rollo = False
