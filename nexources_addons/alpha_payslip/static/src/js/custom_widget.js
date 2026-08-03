/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

class CustomWidget extends Component {
    static template = "alpha_payslip.CustomWidget";
    static props = { ...standardFieldProps };

    get displayValue() {
        const currentValueField = this.props.field?.options?.currentValue;
        const raw = currentValueField
            ? (this.props.record.data[currentValueField] ?? this.props.value)
            : this.props.value;
        const value = raw || 0;
        return value.toString();
    }
}

registry.category("fields").add("custom_widget", {
    component: CustomWidget,
});
