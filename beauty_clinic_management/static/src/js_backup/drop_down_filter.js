import { _t } from "@web/core/l10n/translation";

import { CalendarCommonRender } from "@web/views/calendar/calendar_common/calendar_common_render";

import { useService } from "@web/core/utils/hooks";
import { WarningDialog } from "@web/core/errors/error_dialogs";

import { DateTimeInput } from '@web/core/datetime/datetime_input';
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { MultiRecordSelector } from "@web/core/record_selectors/multi_record_selector";

export class CalendarCommonRenderCustom extends CalendarCommonRender{

    static template = "beauty_clinic_management.CalendarCommonRender";
    static props = {};
    static components = {
        DateTimeInput,
        Dropdown,
        DropdownItem,
        MultiRecordSelector,
    };
    setup(){
        super.setup();

        console.log('=======hello account filter custom from setup=====');
    }


    getMultiRecordSelectorProps(resModel, optionKey) {
        super.getMultiRecordSelectorProps(resModel, optionKey)
    }

    //------------------------------------------------------------------------------------------------------------------
    // Rounding unit
    //------------------------------------------------------------------------------------------------------------------

    //------------------------------------------------------------------------------------------------------------------
    // Generic filters
    //------------------------------------------------------------------------------------------------------------------

    //------------------------------------------------------------------------------------------------------------------
    // Custom filters
    //------------------------------------------------------------------------------------------------------------------


}