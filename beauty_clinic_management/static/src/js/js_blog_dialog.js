/** @odoo-module **/
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";

export class jsClassDialog extends Component{
    clickClose() {
        this.props.close()
    }
}

jsClassDialog.template = "beauty_clinic_management.infoDialog";
jsClassDialog.components = { Dialog };
jsClassDialog.title = _t("Model Info"),
jsClassDialog.props = {
    confirmLabel: { type: String, optional: true },
    confirmClass: { type: String, optional: true },
    resModel: { type: String, optional: true },
    tools: Object,
    close: { type: Function, optional: true },
    };
jsClassDialog.defaultProps = {
    confirmLabel: _t("Close"),
    confirmClass: "btn-primary",
};

