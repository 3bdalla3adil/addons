/** @odoo-module **/

import { registry } from "@web/core/registry";
import { createElement, append } from "@web/core/utils/xml";
import { Notebook } from "@web/core/notebook/notebook";
import { formView } from "@web/views/form/form_view";
import { FormCompiler } from "@web/views/form/form_compiler";
import { FormRenderer } from "@web/views/form/form_renderer";
import { FormController } from '@web/views/form/form_controller';
import { useService } from "@web/core/utils/hooks";

import { calenderView } from "@web/views/calendar/calendar_view";

console.log("===========WidgetController===ODOO 17======")

export class WidgetController extends FormController {
    setup() {
        super.setup();
        console.log("======satup========ODOO 17=====")
    }

    async deleteRecord() {
        if ( !await this.account_move_service.addDeletionDialog(this, this.model.root.resId)) {
            return super.deleteRecord(...arguments);
        }
    }
};

export const WidgetFormView = {
    ...formView,
    Controller: WidgetController,
};

registry.category("views").add("widget_form", WidgetFormView);