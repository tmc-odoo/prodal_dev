{
    'name': 'Rierba ',
    'version': '14.0.1.0.0',
    'summary': 'Desarrollos personalizados Rierba',
    'category': '',
    'author': 'Atrivia SRL',
    'maintainer': 'Atrivia SRL',
    'website': 'atrivia14.odoo.com',
    'license': '',
    'contributors': [
        'Christopher Suazo <christophersuazop@gmail.com>',
    ],
    'depends': [
        'stock', 'sale', 'account', 'repair'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/account_move_views.xml',
        'views/repair_order_views.xml',
        'views/project_task_view.xml',
        'wizards/cash_register_report_wizard_view.xml',
        'reports/reports.xml',
        'reports/cash_register_report_view.xml',
        'reports/report_templates.xml',


    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
