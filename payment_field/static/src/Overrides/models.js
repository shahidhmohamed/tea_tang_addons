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
        var uid = order.uid;
        const tktNumber = order.uid;
        if (this.currentOrder) {
            this.currentOrder.set_tkt_number(tktNumber);
            // console.log("Current Order with Card Number:", this.currentOrder);
        }
        console.log("tkt_number payment", tktNumber)
        const cardNumber = document.getElementById('card_number').value;
        // console.log('Card Number:', cardNumber);

        if (this.currentOrder) {
            this.currentOrder.set_card_number(cardNumber);
            // console.log("Current Order with Card Number:", this.currentOrder);
        }


        super._finalizeValidation()
    }
});

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.card_number = this.card_number || "";
        this.tkt_number = this.tkt_number || "";

    },

    set_card_number(cardNumber) {
        this.card_number = cardNumber;
    },

    set_tkt_number(tktNumber) {
        this.tkt_number = tktNumber;
    },

    get_card_number() {
        return this.card_number;
    },

    get_tkt_number() {
        return this.tkt_number;
    },

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.card_number = this.card_number;  // Include the card number in the exported JSON
        json.tkt_number = this.tkt_number;
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.card_number = json.card_number || "";  // Initialize the card number from the JSON
        this.tkt_number = json.tkt_number || "";
    },
});



