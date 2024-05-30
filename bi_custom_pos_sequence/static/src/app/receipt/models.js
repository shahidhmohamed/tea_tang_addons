/** @odoo-module */

import { Order, Orderline, Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

// New orders are now associated with the current table, if any.
patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.sequence_code = this.sequence_code || "";
    },
    set_seq_code(seq_code) {
        this.sequence_code = seq_code;
    },
    get_seq_code() {
        return this.sequence_code;
    },


});