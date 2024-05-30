# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'POS Customize Kanak',
    'description': """
Customer Select validation
    """,
    "category": "Point Of Sale",
    'license': 'OPL-1',
    "author": "Kanak Infosystems LLP.",
    "website": "https://www.kanakinfosystems.com",
    "depends": ['pos_restaurant', 'pos_hr'],
    'sequence': 400,
    'images': [],
    'data': [
        "views/pos_order_view.xml",
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_customize_kanak/static/src/js/models.js',
            'pos_customize_kanak/static/src/js/PaymentScreen.js',
        ],
        'web.assets_qweb': [
            'pos_customize_kanak/static/src/xml/*.xml',
        ],
    },
    'sequence': 1,
    'installable': True,
    'application': False,
}
