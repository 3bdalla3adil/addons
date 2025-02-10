/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { CalendarController } from "@web/views/calendar/calendar_controller";
import { formView } from '@web/views/form/form_view';
import { calendarView } from '@web/views/calendar/calendar_view';
import { registry } from "@web/core/registry";

import { jsClassDialog } from "@beauty_clinic_management/js/js_blog_dialog";

//class jsClassModelInfo extends FormController {
class jsClassModelInfo extends CalendarController {
   actionInfoForm(){
       this.env.services.dialog.add(jsClassDialog, {
           resModel: this.props.resModel,
           resDesc: "This is a demo pop-up; feel free to customize the functionality to meet your requirements."
       });
   }
}

jsClassModelInfo.template = "beauty_clinic_management.modelInfoBtn";
export const modelInfoView = {
//   ...formView,
   ...calendarView,
   Controller: jsClassModelInfo,
};
registry.category("views").add("model_info", modelInfoView);
