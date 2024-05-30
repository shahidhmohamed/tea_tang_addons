{
  "name"                 :  "POS Receipt Print (LBX)",
  "summary"              :  "This module allows to customize POS Receipts.",
  "category"             :  "Point Of Sale",
  'sequence'             :  2,
  "version"              :  "1.0.1",
  "author"               :  "Levant Business Experts (Pvt) Ltd",
  "license"              :  "Other proprietary",
  "website"              :  "https://levantbizexperts.com/",
  "depends"              :  ['point_of_sale','base'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'demo/demo.xml',
                             'views/pos_config_view.xml',
                             'views/receipt_design_view.xml',
                             'views/res_config_settings.xml',
                            ],
  "assets"               :  {
                              'point_of_sale._assets_pos': [
                                "/pos_receipt_design/static/src/Overrides/**",
                              ],
                            },
  "images"               :  ['static/description/icon.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "pre_init_hook"        :  "pre_init_check",
}
