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
        'views/my_maintenance_activity_types.xml',
        'views/my_maintenance_equipment_categories.xml',
        'views/my_maintenance_equipments.xml',
        'views/my_maintenance_stages.xml',
        'views/my_maintenance_teams.xml',
        'views/my_maintenance_reporting.xml',
        'views/my_maintenance_menu.xml',

    ],
    'demo':[],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}