odoo.define("pos_customize_kanak.sale_types", function(require) {
    "use strict";
    const models = require("point_of_sale.models");

    models.load_fields("pos.order", ["pos_customer_code"]);

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attr, options) {
            this.pos_customer_code = '';
            _super_order.initialize.apply(this, arguments);
        },
        export_as_JSON: function() {
            var json = _super_order.export_as_JSON.call(this);
            json.pos_customer_code = this.pos_customer_code || '';
            return json;
        },
        init_from_JSON: function(json) {
            this.pos_customer_code = json.pos_customer_code || '';
            return _super_order.init_from_JSON.apply(this, arguments);
        },
        export_for_printing: function() {
            var json = _super_order.export_for_printing.apply(this, arguments);
            json.pos_customer_code = this.pos_customer_code;
            return json;
        },
        set_pos_customer_code: function(pos_customer_code){
            this.pos_customer_code = pos_customer_code;
            this.trigger('change', this);
        },
        get_pos_customer_code: function(){
            return this.pos_customer_code;
        },
    });
});