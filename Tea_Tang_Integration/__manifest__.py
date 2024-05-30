{
    'name': 'Tea Tang Ogf Integration',
    'author':'M.SHAHIDH',
    'sequence': 2,
    'summary': 'ogf integration',
    'depends':[
        'point_of_sale',
        'sale',
        'purchase'
    ],
    'data': [
        'views/pos_order.xml',
        'views/pos_order_2.xml',
        'data/data.xml',
        'security/ir.model.access.csv'
        
    ],
    'assets': {
    },
    'installable': True,
    'application': True,
}