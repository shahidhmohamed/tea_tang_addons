/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { _t } from "@web/core/l10n/translation";
import { serializeDateTime } from "@web/core/l10n/dates";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { App, onMounted, useState } from "@odoo/owl";
import { renderToString } from "@web/core/utils/render";
import { useService } from "@web/core/utils/hooks";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";




patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.sequence_code = this.sequence_code || "";
        if (!this.validation_date) {
            this.validation_date = serializeDateTime(this.date_order)
        }

        // Check if the name is being set to "Order %s" and remove "Order" part
        if (this.name && this.name.startsWith("Order ")) {
            this.name = this.name.replace("Order ", "");
        }


    },
    set_seq_code(seq_code) {
        this.sequence_code = seq_code;
    },
    get_seq_code() {
        return this.sequence_code;
    },

    export_for_printing() {
        var dict = super.export_for_printing(...arguments);
        dict.company = this.pos.company;
        dict.rOrder = this;
        dict.sequence_code = this.sequence_code;

        return dict;
    }
});


patch(PosStore.prototype, {
    async _processData(loadedData) {
        await super._processData(...arguments);
        this._loadReceiptDesign(loadedData['receipt.design']);
    },
    _loadReceiptDesign(designs) {
        this.db.all_designs = designs;
        var receipt_by_id = {};
        designs.forEach(function (design) {
            receipt_by_id[design.id] = design;
        });
        this.db.receipt_by_id = receipt_by_id;
    }
});

patch(OrderReceipt.prototype, {
    setup() {
        super.setup(); // Call the parent class's setup method
        this.orm = useService("orm");
        this.state = useState({ template: true });
        this.pos = useService("pos");

        onMounted(async () => {
            var self = this;
            var env = self.env;
            if (env.services.pos.config.use_custom_receipt) {
                var receipt_design_id = env.services.pos.config.receipt_design_id[0];
                var receipt_design = env.services.pos.db.receipt_by_id[receipt_design_id].receipt_design;
                var order = this.props.data.rOrder;


                var pos_order = this.pos.pos_order


                // console.log("this pos data", this.pos)






                // Initialize variables to store order lines data
                var orderLinesData = [];
                var totalQuantity = 0;

                // Loop through each order line to collect data
                order.get_orderlines().forEach(function (orderline) {
                    var unitPriceBeforeDiscount = orderline.get_unit_price();
                    totalQuantity += orderline.quantity;

                    // Push data of each order line to the array
                    orderLinesData.push({
                        productName: orderline.get_product().display_name,
                        unitPriceBeforeDiscount: unitPriceBeforeDiscount,
                        quantity: orderline.quantity,
                        amount: orderline.get_price_with_tax(),
                        discount: orderline.discount,
                        customer_note: orderline.customer_note
                    });


                });

                const receiptDate = order.date_order;
                const dateObject = new Date(receiptDate);
                const orderDateFormatted = dateObject.toLocaleDateString();
                const orderTimeFormatted = dateObject.toLocaleTimeString('en-US', {
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: true
                });

                const cashier_name = order.cashier.name;
                const cardNumber = order.card_number;
                const tktNumber = order.tkt_number;
                console.log("tktNumber", tktNumber)


                var data = {
                    widget: self.env,
                    pos: order.pos,
                    order: order,
                    receipt: order.export_for_printing(),
                    orderlines: orderLinesData,
                    paymentlines: order.get_paymentlines(),
                    totalItems: orderLinesData.length,
                    totalQuantity: totalQuantity,
                    pos_order: pos_order,
                    cardNumber: cardNumber,
                    tktNumber: tktNumber,
                    receipt_date: orderDateFormatted,
                    receipt_time: orderTimeFormatted
                };

                // console.log("data:", data)


                var parser = new DOMParser();
                var strtemplate = '<templates><t t-name="receipt_design">' + receipt_design + '</t></templates>';
                var xmlDoc = parser.parseFromString(strtemplate, "text/xml");
                var template = xmlDoc.querySelectorAll("templates > [t-name]")[0];

                // Add the receipt template to the rendering app
                const app = renderToString.app;
                app.addTemplate("receipt_design", template);

                // Render the receipt using the data
                var receipt = await renderToString("receipt_design", data);
                $('div.pos-receipt').html(receipt);
            }
        });
    },
    /**
     * For accessibility, pressing <space> should be like clicking the product.
     * <enter> is not considered because it conflicts with the barcode.
     *
     * @param {KeyPressEvent} event
     */

    async seq_data() {
        var self = this;
        let order = self.pos.get_order();
        await this.orm.call(
            'pos.order',
            'create_pos_receipt_sequence',
            [0, order.pos_session_id],

        ).then(function (seq_code) {
            order.set_seq_code(seq_code)
        })

    },
    get sequence() {
        var self = this;
        let order = self.pos.get_order();
        return order.sequence_code

    },
});

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        this.orm = useService("orm");
        this.isValidationInProgress = false; // Flag to prevent multiple submissions
    },

    /**
     * For accessibility, pressing <space> should be like clicking the product.
     * <enter> is not considered because it conflicts with the barcode.
     *
     * @param {KeyPressEvent} event
     */

    async _finalizeValidation() {
        if (this.isValidationInProgress) {
            return; // Exit if a validation is already in progress
        }

        this.isValidationInProgress = true;

        var self = this;
        var order = this.currentOrder;
        var uid = order.uid;
        var newseq = ("T") + uid;
        // console.log("Hello Uid", newseq)

        try {
            const result = await this.orm.call(
                'pos.order',
                'create_pos_receipt_sequence',
                [0, this.currentOrder.pos_session_id]
            );
            // console.log("POS receipt sequence created successfully.");
            // console.log("Sequence called:", newseq);
            // console.log("ORM call result:", result);

            // Update order.name with the result
            order.name = result;
            // console.log("Order name updated:", order.name);
        } catch (error) {
            // console.error("Error creating POS receipt sequence:", error);
        } finally {
            super._finalizeValidation();
            this.isValidationInProgress = false;
        }
    },
});

// patch(TicketScreen.prototype, {
//     setup() {
//         super.setup();
//         this.pos = usePos();

//         // Log the cashier's name for the current order when the TicketScreen is set up
//         const currentOrder = this.pos.get_order();
//         console.log(this.getCashier(currentOrder));
//     },
//     getCashier(order) {
//         const new_cashier = order.user_id
//         // Ensure that the order has a valid cashier field
//         // return order && order.cashier ? order.cashier.name : "";
//         return new_cashier
//     }
// });