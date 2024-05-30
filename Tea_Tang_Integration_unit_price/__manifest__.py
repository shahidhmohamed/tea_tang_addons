{
    'name': 'Tea Tang Unit Price',
    'author':'M.SHAHIDH',
    'sequence': 2,
    'summary': 'Get Unit Price For Lines',
    'depends':[
        'point_of_sale',
        'sale',
        'purchase'
    ],
    'data': [
        'views/purchase_order.xml',
        'data/data.xml',
        'security/ir.model.access.csv'
        
    ],
    'assets': {
    },
    'installable': True,
    'application': True,
}