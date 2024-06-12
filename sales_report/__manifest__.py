{
    'name': 'sales_report',
    'author':'M.SHAHIDH',
    'sequence': 6,
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
        'wizard/pos_details.xml',
        'views/purchase_order.xml',
        'security/ir.model.access.csv',
        'views/action_report.xml',
        'views/report.xml',
        
    ],
    'assets': {
    },
    'installable': True,
    'application': False,
}