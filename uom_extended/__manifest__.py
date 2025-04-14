{
    'name': 'UOM Extended',
    'version': '1.0',
    'author':'ANFEPI: Roberto Requejo Fernández',
    'depends': ['base', 'mrp'],
    'description': """
Custom calculated fields
========================

    """,
    'data': [
        'views/product_product_view.xml',
        'views/stock_move_view.xml',
        'views/stock_lot_view.xml',
        'views/stock_move_line_view.xml'
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    "license": "AGPL-3",
}