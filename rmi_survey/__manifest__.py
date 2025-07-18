# -*- coding: utf-8 -*-
{
    'name': "RMI Survey",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'marketing',
    'version': '0.1',
    'lisence': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','survey', 'board'],

    # always loaded
    'data': [
        'data/rmi.final_rating.csv',
        'data/rmi.komposit_risiko.csv',
        'data/rmi.param_dimensi.csv',
        'data/rmi.param_group.csv',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/aspek_kinerja.xml',
        'views/param_dimensi.xml',
        'views/param_group.xml',
        'views/final_rating.xml',
        'views/komposit_risiko.xml',
        'views/survey_inherit_view.xml',
        'views/res_branch_view.xml',
        'views/dashboard.xml',
        'reports/report_rekomendasi.xml',
        'reports/report_rmi.xml',
        'views/interest_coverage_ratio.xml',
        'views/survey_login_required.xml'
    ],

    'assets': {
        'web.assets_backend': [
            'rmi_survey/static/src/components/**/*.js',
            'rmi_survey/static/src/components/**/*.xml',
            'rmi_survey/static/src/components/**/*.scss',
        ],
    },

    'installable': True,
    'application': True,
}
