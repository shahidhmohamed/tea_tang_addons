{
  "name"                 :  "KOT UID (LBX)",
  "summary"              :  "Custom Field For Pos Payment",
  "category"             :  "Point Of Sale",
  'sequence'             :  3,
  "author"               :  "Levant Business Experts (Pvt) Ltd",
  "website"              :  "https://levantbizexperts.com/",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/pos_order.xml'
                            ],
  "assets"               :  {
                              'point_of_sale._assets_pos': [
                                "kot_uid/static/src/Overrides/**",
                              ],
                            },
  "images"               :  ['static/description/icon.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}
