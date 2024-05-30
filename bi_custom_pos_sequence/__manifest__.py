{
    'name': "POS Order Custom Sequence | POS Receipt Sequence",
    'version': '17.0.0.0',
    'sequence':1,
    'category': 'Point of Sale',
    'summary': "POS Order Sequence POS custom Sequence POS custom Receipt Sequence POS Personalized Sequence point of sales custom Sequence on POS Sequence point of sales receipt Sequence point of sales Personalized Sequence on pos receipt custom sequence on point of sale",
    'description': """ POS Custom Receipt Sequence Odoo App helps users to managing and organizing receipts with customized sequence number for point of sale operation. Users can easily customize their receipts number and set them up in a specific sequence that suits business needs. Users have option to enable or disable custom sequence for receipt and print, also visible in order view. """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.com',
    "price": 15,
    "currency": 'EUR',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/res_config_settings.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'bi_custom_pos_sequence/static/src/app/receipt/models.js',
            'bi_custom_pos_sequence/static/src/app/receipt/orderreceipt.js',
            'bi_custom_pos_sequence/static/src/app/receipt/orderreceipt.xml',
            'bi_custom_pos_sequence/static/src/app/receipt/paymentscreen.js',
           
        ],
    },
    'license':'OPL-1',
    'application':True,
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/Wa5hS7FXdWk',
    "images":["static/description/Banner.gif"],
}

