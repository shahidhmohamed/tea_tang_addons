{
    'name': 'Inter Compant Transaction',
    'author':'M.SHAHIDH',
    'sequence': 5,
    'summary': 'Get Inter Compant Transaction Value',
    'depends':[
        'stock',
        'stock_account',
        'product',
        'purchase',
        'stock_account'
    ],
    'data': [
        'views/stock_picking_views.xml',
        'views/product_template_views.xml',
        'security/ir.model.access.csv'
        
    ],
    'assets': {
    },
    'installable': True,
    'application': True,
}