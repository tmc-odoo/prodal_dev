{
    'name': 'Rierba Sale',
    'version': '14.0.1.0.0',
    'summary': 'Add features and enhancements to the "Sale" module',
    'category': 'sale',
    'author': 'Atrivia SRL',
    'maintainer': 'Atrivia SRL',
    'website': 'atrivia14.odoo.com',
    'license': '',
    'contributors': [
    ],
    'depends': [
        'sale_management', 'stock', 'account','web_domain_field'
    ],
    'data': [
        'views/product_template.xml',
        'views/sale_order.xml',
        'views/account_move.xml',
        'views/stock_picking.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
