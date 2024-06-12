{
    'name': 'Receipt Reprint LBX',
    'sequence': 4,
    'author':'M.SHAHIDH',
    'depends': ['account'],
    'data': [
            #  'views/pos_inherit.xml',
             'report/re_print.xml',
             'report/report_1.xml',
            #  'views/template.xml',
            ],
    'assets': {
        # 'web.report_assets_common': [
        #     'reprint_download/static/src/scss/**/*',
        #     'reprint_download/static/src/css/font.css',
        # ],
    },
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
