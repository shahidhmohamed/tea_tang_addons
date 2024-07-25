/**@odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { Order } from "@point_of_sale/app/store/models";



patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        this.orm = useService("orm");
    },

    async _finalizeValidation() {
        var self = this;
        var order = this.currentOrder;
        const tktNumber = order.uid;
        // console.log('Card Number:', cardNumber);

        if (this.tktNumber) {
            this.currentOrder.set_tkt_number(tktNumber);
            // console.log("Current Order with tkt Number:", this.currentOrder);
        }

        console.log("tkt_number payment", tktNumber)

        super._finalizeValidation()
    }
});

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.tkt_number = this.tkt_number || "";

    },

    set_card_number(tktNumber) {
        this.tkt_number = tktNumber;
    },

    get_tkt_number() {
        return this.tkt_number;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.tkt_number = this.tkt_number;  // Include the card number in the exported JSON
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.tkt_number = json.tkt_number || "";  // Initialize the card number from the JSON
    },
});



