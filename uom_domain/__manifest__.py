
{
    'name': 'Filtro de Unidad de Medida Secundaria',
    'version': '1.0',
    'summary': 'Agrega un dominio para unidades de medida secundarias en compras y ventas',
    'author':'ANFEPI: Roberto Requejo Fernández',
    'category': 'Purchases',
    'depends': ['purchase', 'sale', 'stock', 'product_uoms_rel'],
    'data': [
        'views/purchase_order_form.xml',
        'views/sale_order_form.xml',
    ],
    'installable': True,
    'images': ['static/description/icon.png'],
    'application': False,
}
