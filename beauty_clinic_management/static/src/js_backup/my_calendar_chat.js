/** @odoo-module **/


import { CalendarRenderer } from '@web/views/calendar/calendar_renderer';
import { calendarView } from "@web/views/calendar/calendar_view";
import { CalendarController } from "@web/views/calendar/calendar_controller";
import { CalendarArchParser } from "@web/views/calendar/calendar_arch_parser";
import { CalendarModel } from "@web/views/calendar/calendar_model";
import { CalendarCommonRenderer } from "@web/views/calendar/calendar_common/calendar_common_renderer";
import { CalendarCommonPopover } from "@web/views/calendar/calendar_common/calendar_common_popover";
import session from 'web.session';

import { Dialog } from 'web.OwlComponents';
import { useService } from "@web.core";
import { useEffect, useEnv, useSubEnv } from "@web.OwlHooks";
import { qweb, _t } from "web.core";
const { sprintf } = owl.utils;
import ajax from "web.Ajax";
import { patch } from "web.Core";

var rpc = require('web.rpc');


console.log('===++++++++++++++++++++++++++++' ,CalendarRenderer)
console.log('===++++++++++++++++++++++++++++' ,calendarView)