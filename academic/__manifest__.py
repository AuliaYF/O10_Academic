# -*- coding: utf-8 -*-
{
    'name': "Academic Information System",

    'description': """
        Academic Information System
    """,

    'author': "auliayf@gmail.com",
    'website': "https://github.com/AuliaYF/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Education',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    'application': True,
    'auto_install': False,
    'installable': True,

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
