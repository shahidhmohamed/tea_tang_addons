odoo.define('pos_customize_kanak.PaymentScreen', function(require) {
    'use strict';

    var Gui = require('point_of_sale.Gui');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { _lt } = require('@web/core/l10n/translation');

    var core = require('web.core');
    var _t = core._t;
    const PaymentScreenCustomerCode = (PaymentScreen) =>
        class extends PaymentScreen {
            async validateOrder(isForceValidate) {
                var pos_customer_code = $("#pos_customer_code").val();
                const order = this.env.pos.get_order();
                if (pos_customer_code.length) {
                    order.set_pos_customer_code(pos_customer_code);
                    return super.validateOrder();
                } else {
                    await this.showPopup('ErrorPopup', {
                        title: this.env._t('Warning'),
                        body:
                            this.env._t('Order Number is required. Please enter the Order Number.'),
                    });
                    return false
                }
            }
        };

    Registries.Component.extend(PaymentScreen, PaymentScreenCustomerCode);

    return PaymentScreenCustomerCode;
});
