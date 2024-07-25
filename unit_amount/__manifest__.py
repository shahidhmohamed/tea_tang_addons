{
    'name': 'Tea Tang Unit Amount ',
    'author':'M.SHAHIDH',
    'sequence': 5,
    'depends':[
        'point_of_sale',
        'sale',
        'purchase',
        'stock',
        'stock_account',
        'product',
        'purchase',
        'stock_account'
    ],
    'data': [
        'views/purchase_order.xml',
        # 'views/purchase_order_template.xml',
        'security/ir.model.access.csv'
        
    ],
    'assets': {
    },
    'installable': True,
    'application': True,
}