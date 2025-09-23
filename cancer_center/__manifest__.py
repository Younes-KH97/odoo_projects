{
    'name': 'cancer_center',
    'version': '1.0',
    'description': '',
    'category': 'custom_modules/anti_cancer_center',
    'depends': [
        'base'
    ],
    'data':[
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/protocol_view.xml',
        'views/medication_view.xml',
        'views/patient_view.xml',
        'views/protocol_assignment.xml',
        'views/protocol_assignment_detail.xml',
        'views/cure_view.xml',
        'views/reaction_view.xml',
        # 'views/cure_statistics_view.xml',
        'views/cancer_center_menus.xml'
    ],
    
    # 'assets': {
    #     'web.assets_backend':[
    #         'cancer_center/static/src/css/statsView.scss',
    #         'cancer_center/static/src/js/statsView.js',
    #         'cancer_center/static/src/xml/statsView.xml',
    #     ]

    # },
    'application': True
}


