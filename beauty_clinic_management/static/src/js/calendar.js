/** @odoo-module **/

import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

import { _t } from "@web/core/l10n/translation";

import { RPCError } from '@web/core/network/rpc_service';
import { sprintf } from "@web/core/utils/strings";
import { onWillStart } from "@odoo/owl";

import { calendarView } from "@web/views/calendar/calendar_view";
import { CalendarController } from "@web/views/calendar/calendar_controller";
import { ListController } from "@web/views/list/list_controller";
import { CalendarCommonRenderer } from "@web/views/calendar/calendar_common/calendar_common_renderer";
import { CalendarQuickCreate } from "@calendar/views/calendar_form/calendar_quick_create";
import { CalendarCommonPopover } from "@web/views/calendar/calendar_common/calendar_common_popover";
import { CalendarModel } from "@web/views/calendar/calendar_model";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

import { useEffect, useEnv, useSubEnv } from "@odoo/owl";
import { session } from "@web/session";
import { Dialog } from "@web/core/dialog/dialog";

console.log("===========CalendarController====CalendarController======",CalendarController)

//MAIN CLASS
//======================Update FormController View=====================

//===========================================================================

// Define and register the beauty_calendar class
export class BeautyCalendarController extends CalendarController {
    setup() {
        super.setup();

        console.log("=====setup======BeautyCalendarController=========");
    }
}

// Create the beauty_calendar view
export const beauty_calendar = {
    ...calendarView,
    Controller: BeautyCalendarController,
//    Renderer: CalendarCommonRenderer,
};

// Register the beauty_calendar view
registry.category("views").add("beauty_calendar", beauty_calendar);
