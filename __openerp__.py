# -*- coding: utf-8 -*-
# =============================================================================
# title           :__openerp__.py
# description     :Manifest file for the gm_syndicat addon
# author          :Louis Marchand
# date            :20180301
# version         :0.1
# notes           :
# python_version  :2.7.12
# =============================================================================


{
    'name': "Gestion des membres (Syndicat)",

    'summary': """Gère les membres du syndicat""",

    'description': """
        Permet la gestion de la base de donnée de membres du Syndicat
        """,

    'author': "Louis Marchand",
    'website': "https://www.seecd.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/gestion_membres.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
