{
    'name': 'Tea Tang Ogf Integration',
    'author':'M.SHAHIDH',
    'sequence': 2,
    'summary': 'ogf integration',
    'depends':[
        'point_of_sale',
        # 'mail',
    ],
    'data': [
        'views/pos_order.xml',
        'views/pos_order_2.xml',
        'data/data.xml',
        'views/setting.xml',
        'security/ir.model.access.csv'
        
    ],
    'assets': {
    },
    'installable': True,
    'application': True,
}