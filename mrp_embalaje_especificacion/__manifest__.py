{
    'name': 'MRP Embalaje Especificacion',
    'version': '1.0',
    'author':'ANFEPI: Roberto Requejo Fernández',
    'depends': ['mrp', 'sale'],
    'summary': 'Extend MRP Production to calculate packaging details from sale orders.',
    'description': """
        This module extends the MRP Production process by extracting packaging details from related sale orders.
        If the sale order's order lines share the same packaging, it calculates and sets the tarimas field accordingly.
        If they differ, it computes the required number of packings per packaging type and creates detailed records.
    """,
    'data': [
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    "license": "AGPL-3",
}