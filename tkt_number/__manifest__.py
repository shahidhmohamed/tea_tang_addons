{
  "name"                 :  "POS Tkt Number (LBX)",
  "summary"              :  "This module allows to customize POS Receipts.",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0.1",
  'sequence'             :  4,
  "website"              :  "https://levantbizexperts.com/",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/pos_order.xml',
                            ],
  "assets"               :  {
                              'point_of_sale._assets_pos': [
                                "/tkt_number/static/src/Overrides/**",
                              ],
                            },
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}
