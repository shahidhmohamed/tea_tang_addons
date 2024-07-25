{
    'name': 'Odoo Online Custom Receipt',
    'author':'M.SHAHIDH',
    'sequence': 6,
    'depends':[
        'point_of_sale',
    ],
    'data': [
        'security/ir.model.access.csv'
        
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'online_receipt/static/src/xml/receipt_template.xml',
        ],
    },
    'installable': True,
    'application': True,
}