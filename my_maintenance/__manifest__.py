# -*- coding: utf-8 -*-
{
    'name': 'My Maintenance ',
    'summary': ' My Maintenance Sotfware  ',
    'description': '''My Maintenance Software
    ''',
    'sequence': -101,
    'version': '1.0',
    'category': 'Productivity',
    'website': 'https://www.odoomates.tech',
    'depends': [
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/my_maintenance_dashboard.xml',
        'views/my_maintenance.xml',
        'views/my_maintenance_activity_type.xml',
        'views/my_maintenance_equipment_category.xml',
        'views/my_maintenance_equipment.xml',
        'views/my_maintenance_stage.xml',
        'views/my_maintenance_team.xml',
        'views/my_maintenance_report.xml',
        'views/my_maintenance_menu.xml',

    ],
    'demo':[],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}