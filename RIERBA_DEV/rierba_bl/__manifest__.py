# -*- coding: utf-8 -*-
{
    'name': "rierba_bl",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'purchase',
        'rierba',
        'project',
        'mail', 
        'account', 
        'stock_landed_costs', 
        'web_domain_field'
    ],

    # always loaded
    'data': [
        'security/group_bl_security.xml',
        'security/ir.model.access.csv',
        'wizards/group_bl_wizard_view.xml',
        'views/purchase_views.xml',
        'views/templates.xml',
        'views/account_move_views.xml',
        'views/stock_landed.xml',

    ],
    # only loaded in demonstration mode

    'installable': True,
    'auto_install': False,
    'application': True
}
