///** @odoo-module **/
//
//import { _t } from "@web/core/l10n/translation";
//
//import { RPCError } from '@web/core/network/rpc_service';
//import { sprintf } from "@web/core/utils/strings";
//import { useService } from "@web/core/utils/hooks";
//import { onWillStart } from "@odoo/owl";
//import { patch } from "@web/core/utils/patch";
//
//import { calendarView } from "@web/views/calendar/calendar_view";
//import { CalendarController } from "@web/views/calendar/calendar_controller";
//import { CalendarCommonRenderer } from "@web/views/calendar/calendar_common/calendar_common_renderer";
//import { CalendarQuickCreate } from "@calendar/views/calendar_form/calendar_quick_create";
//import { CalendarCommonPopover } from "@web/views/calendar/calendar_common/calendar_common_popover";
//import { CalendarModel } from "@web/views/calendar/calendar_model";
//import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
//
//import { useEffect, useEnv, useSubEnv } from "@odoo/owl";
//import { session } from "@web/session";
//import { Dialog } from "@web/core/dialog/dialog";
//
//
//patch(CalendarCommonPopover.prototype, {
//    setup () {
//        super.setup();
//        // this.canInvoice = false;
//        this.canPayment = false;
//        this.actionService = useService("action");
//        if('is_invoice_state' in this.props.record.rawRecord){
//            this.canInvoice = this.props.record.rawRecord.is_invoice_state;
//            this.canOrder = this.props.record.rawRecord.is_invoice_state;
//        }
//
//        console.log(this, "popover");
//        if('invoice_amount' in this.props.record.rawRecord && 'invoice_paid' in this.props.record.rawRecord){
//            var invoice_amount = this.props.record.rawRecord.invoice_amount
//            var invoice_paid = this.props.record.rawRecord.invoice_paid
//            console.log(invoice_amount, invoice_paid, "paid")
//
//            if(invoice_amount == invoice_paid){
//                if(invoice_paid > 0){
//                    this.canPayment = true;
//                }
//            }
//        }
//    },
//
//    _onClickOrderOpen: function (ev) {
//        var self = this;
//        console.log(ev)
//        console.log(self)
//        var context = {'default_appointment_id': parseInt(self.props.record.id)};
//        self.props.close();
//        return self.actionService.doAction({
//            name: 'Create: Sale Order',
//            type: 'ir.actions.act_window',
//            //res_model: 'calender.invoice.wizard',
//            res_model: 'calender.sale.wizard',
//            target: 'new',
//            views: [[false, 'form']],
//            context: context,
//        });
//    },
//
//    _onClickInvoiceOpen: function (ev) {
//        var self = this;
//        console.log(ev)
//        console.log(self)
//        var context = {'default_appointment_id': parseInt(self.props.record.id)};
//        self.props.close();
//        return self.actionService.doAction({
//            name: 'Create: Invoices',
//            type: 'ir.actions.act_window',
//            res_model: 'calender.invoice.wizard',
//            target: 'new',
//            views: [[false, 'form']],
//            context: context,
//        });
//    },
//
//    _onClickPaymentOpen: function (ev) {
//        var self = this;
//        var context = {'default_appointment_id': parseInt(self.props.record.id)};
//        self.props.close();
//        return self.actionService.doAction({
//            name: 'Register Payment',
//            type: 'ir.actions.act_window',
//            res_model: 'calender.payment.wizard',
//            target: 'new',
//            views: [[false, 'form']],
//            context: context,
//        });
//    },
//
//    _onClickNotesOpen: function (ev) {
//        var self = this;
//        var context = {'default_appointment_id': parseInt(self.props.record.id)};
//        self.props.close();
//        return self.actionService.doAction({
//            name: 'Create: Notes',
//            type: 'ir.actions.act_window',
//            res_model: 'calender.notes.wizard',
//            target: 'new',
//            views: [[false, 'form']],
//            context: context,
//        });
//    },
//
//    _onClickChartOpen: function (ev) {
//        ev.preventDefault();
//        var self = this;
//        var context = {'default_appointment_id': parseInt(self.props.record.id)};
//        self.props.close();
//        return self.actionService.doAction({
//            name: 'Face/Body Chart',
//            type: 'ir.actions.client',
//            tag: 'face_body_chart',
//            target: 'current',
//            context: context,
//        });
//    },
//
//    async get_events() {
//        var self = this;
//        await this.__owl__.bdom;
//        $('.o_popover_container').find('.o_cw_popover_order_m').bind("click", {real_obj: self}, self._onClickOrderOpen)
//        $('.o_popover_container').find('.o_cw_popover_invoice_m').bind("click", {real_obj: self}, self._onClickInvoiceOpen)
//    },
//
//    dateToServer (date, fieldType) {
//        date = date.clone().locale('en');
//        if (fieldType === "date") {
//            return date.local().format('YYYY-MM-DD');
//        }
//        return date.utc().format('YYYY-MM-DD HH:mm:ss');
//    }
//
//
//});
//
//    //DONE!
//
//    //========================================================================================
//    //========================================================================================
//
//patch(CalendarCommonRenderer.prototype, {
//    //DONE!
//    setup () {
//        super.setup();
//
//        this.rpc = useService("rpc");
//        this.actionService = useService("action");
//        this.dialogService = useService("dialog");
//
//            if (this.props.model.meta.resModel && this.props.model.meta.resModel=='medical.appointment'){
//                useEffect(() => {
//                    this.get_clinics_slot_details();
//                    //=================================================================
//                    //var $eventTitle = $event.find('.o_event_title.text-truncate');
//                    //if ($eventTitle.length) { $eventTitle.removeClass('text-truncate');}
//                    // ================================================================
//            });
//        }
//    },
//
//    //    ==================================================================================================
//    //    ==================================================================================================
//
//    //    ==================================================================================================
//    //    ==================================================================================================
//
//    //DONE!
//    _displayTimeSlots: async function (e) {
//
//        var date_time = e.data.real_obj.props.model.data.range.start.toString();
//        var t = date_time.split(/[- :]/);
//        var date = new Date(date_time);
//        var target_date = date.toString();
//        //  await this._rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot',{
//         await this._rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot',{
//            model: 'clinic.slot',
//            method: 'get_clinics_slot',
//            args: [target_date.split(' (')[0], e.currentTarget.id],
//            kwargs: {context: e.data.real_obj.props.model.meta.context}//self.context,
//        }).then(function (clinicResult) {
//            if (clinicResult) {
//
//                var dtime_slots = clinicResult[0].time_slots
//                var doc_name = clinicResult[0].name
//
//                var a ='';
//                for (var k =0; k < dtime_slots.length; k++) {
//                    a += dtime_slots[k].start_hour + ' to ' + dtime_slots[k].end_hour + " ";
//                }
//                 e.data.real_obj.dialogService.add(ConfirmationDialog, {
//                    body:  a,
//                    title:  _t("Time Slots of " + doc_name),
//                    confirm: () => {},
//                });
//            }
//        });
//    },
//    //DONE!
//    _fcWidgetContent: async function (ev) {
//        // var self = this;
//        var date_time = ev.data.real_obj.props.model.data.range.start.toString();
//        var t = date_time.split(/[- :]/);
//        var date = new Date(date_time);
//        var target_date = date.toString();
//        var context = {};
//        if(ev.currentTarget.id){
//            context['default_clinic_id'] = parseInt(ev.currentTarget.id) || false;
//        }
//        else if(ev.target.id){
//            context['default_clinic_id'] = parseInt(ev.target.id) || false;
//        }
//        context['from_time'] = ev.currentTarget.dataset.time || $(ev.target).parent()[0].dataset.time;
//        context['dateToString'] = target_date.split(' (')[0];
//        await ev.data.real_obj.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot_validation',{
//            model: 'clinic.slot',
//            method: 'get_clinics_slot_validation',
//            args: [target_date.split(' (')[0], ev.currentTarget.id],
//            kwargs: {context: context}
//        }).then(function (result) {
//            if(result){
//                ev.data.real_obj.actionService.doAction({
//                    name: 'Create: Appointments',
//                    type: 'ir.actions.act_window',
//                    res_model: 'calender.appointment.wizard',
//                    target: 'new',
//                    views: [[false, 'form']],
//                    context: context,
//                });
//            }else{
//
//                var content ='Appointment Slot is not available.';
//
//                ev.data.real_obj.dialogService.add(ConfirmationDialog, {
//                    body:  content,
//                    title:  _t("Alert"),
//                    confirm: () => {},
//                });
//            }
//        })
//    },
//
//    async get_clinics_slot_details_rpc(eventName,clinic_id,j) {
//        var self = this;
//
//        await self.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot_validation',{
//            model: 'medical.appointment',
//            method: 'get_data',
//            args: [false, clinic_id, eventName, j],
//            kwargs: {context: []}
//        }).then(function (result) {
//        console.log("=============res111=============",result)
//        })
//    },
//
//    // DONE
//    async get_clinics_slot_details(checkResizeWindow) {
//        var $containerHeight = $(window).height();
//        var self = this;
//
//        var date_time = self.props.model.data.range.start.toString();
//        var t = date_time.split(/[- :]/);
//        var date = new Date(date_time);
//        var target_date = date.toString();
//
//        await this.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot',{
//            model: 'clinic.slot',
//            method: 'get_clinics_slot',
//            args: [target_date.split(' (')[0]],
//            kwargs: {context: self.props.model.meta.context}//self.context,
//        }).then(function (result) {
//
//            if (result) {
//                $(self.fc.el.parentNode).find('.fc-time-grid-container').css({
//                    'overflow': 'scroll',
//                    'margin-top': '20%',
//                    'position': 'relative',
//                })
//                var rl = result.length * 280;
//                if (rl <= 1400) {
//                    rl = 1400;
//                }
//                $(self.fc.el.parentNode).find('.fc-time-grid').addClass("row");
//                $(self.fc.el.parentNode).find('.fc-time-grid').css({
//                   'width' : rl + 'px',
//                   'position': 'relative',
//                   'height': '-webkit-fill-available',
//                });
//                var s = $(self.fc.el.parentNode).find('.fc-slats').slice(1).remove();
//                $(self.fc.el.parentNode).find('.fc-slats').addClass("originalTimeslot");
//                $(self.fc.el.parentNode).find('.fc-slats').css({'width': '260px','z-index': '0'});
//                //G.T CODE
//                $(self.fc.el.parentNode).find('.fc-widget-content').css({'margin-top':'-280px'})
//
//                //  This code is used for hide the tr and its td if this operation not perform then
//                //  our td click event not work every time
//                $(self.fc.el.parentNode).find('.fc-bg').css({
//                      'display': 'none',
//                    });
//                $(document).ready(function() {
//                    $('.fc-resizer.fc-end-resizer').next('.fc-bg').css('display', 'block');
//                });
//
//                var preNode = false;
//                var s = $(self.fc.el.parentNode).find('div.fc-slats');
//
//                // This is used for set the width of appointment create
//                //G.T CODE
//                var gridEvent = $(self.fc.el.parentNode).find('a.fc-time-grid-event').css({
//
////                    "width": "200px",
//                    "width": "100%",
//                    "font-weight":"bold",
//                    "z-index": "1",
//                    "padding-top": "0px",
//                    "margin-top": 0 + '%',
//                    "cursor": "pointer",
//
//                })
//
//                //here fix
//                if($(self.fc.el.parentNode).find('a.fc-time-grid-event').length){
//                    $.each($(self.fc.el.parentNode).find('a.fc-time-grid-event'), function(e,i){
//                        var top_css = $(i).css("top")
//                        var top_a = top_css;
//                        var top_b = top_a.replace("px", "");
//                        var top_c = parseInt(top_b) - 40;
//                        var top_d =  top_c.toString() + 'px';
//                        $(i).css("top",top_d)
//
//                        var bottom_css = $(i).css("bottom")
//                        var bottom_a = bottom_css;
//                        var bottom_b = bottom_a.replace("px", "");
//                        var bottom_c = parseInt(bottom_b) + 40;
//                        var bottom_d =  bottom_c.toString() + 'px';
//                        $(i).css("bottom",bottom_d)
//                    })
//                }
//
//                var divHeight = '20px';
//                for (var j =0; j < result.length; j++) {
//                    console.log("=================2=============",s)
//                    $.each(s, function(e,i){
//                        var trList = $(i).find('table').find('tbody').find('tr');
//                        var trFirst = $(i).find('table').find('tbody').find('tr:eq(0)');
//                        var trSecond = $(i).find('table').find('tbody').find('tr:eq(1)');
//                        divHeight = trFirst.height() + trSecond.height() + 20 + 'px';
//                        trFirst.css({'display': 'none'});
//                        trSecond.css({'display': 'none'});
//                    })
//                }
//                $('.displayTimeSlots').addClass('d-none')
//                for (var j =0; j < result.length; j++) {
//                    if (j == 0) {
//
//                        var clinicName = result[j].name;
//                        $(self.fc.el.parentNode).find('.fc-slats').attr('id', result[j].id);
//                        var clinicDetails = 'clinicDetails_' + j + '_' + result[j].id;
//                        var newDynamicClass = 'mypopshow_' + j + '_' + result[j].id;
//                        var clinicDiv = $("<div id="+result[j].id+" class=" + clinicDetails +"><strong style='margin-bottom:0px'> "+ result[j].name +
//                        "</strong></span>");
//
//                        var dtime_slots = result[j].time_slots
//                        var a ='';
//                        var slot_length = dtime_slots.length
//                        for (var k =0; k < dtime_slots.length; k+=2) {
//                            if(k<4){
//                                a += "<p style='font-size: 12px;margin-bottom:0px;color: darkgreen;font-weight: bold;'>"
//                                if(k<slot_length){
//                                    a += dtime_slots[k].start_hour + ' to ' + dtime_slots[k].end_hour
//                                }
//
//                                 if(k+1<slot_length){
//                                    a += ', ' + dtime_slots[k+1].start_hour + ' to ' + dtime_slots[k+1].end_hour
//                                }
//                                a += "</p>";
//                            }
//                        }
//
//                        clinicDiv.append(a)
//                        clinicDiv.addClass('displayTimeSlots');
//
//                        $(self.fc.el.parentNode).find('.fc-slats').before(clinicDiv);
//                    }
//                    else {
//                        var copyTimeSlot = $('.originalTimeslot').clone();
//                        copyTimeSlot.removeClass("originalTimeslot");
//                        var clinicName = result[j].name;
//                        var clinicDetails = 'clinicDetails_0_' + result[0].id;
//                        var currentClinicDetails = 'clinicDetails_' + j + '_' + result[j].id;
//
//                        copyTimeSlot.find('div.' + clinicDetails).remove()
//                        if (!preNode) {
//                            preNode = copyTimeSlot.attr('id', result[j].id).insertAfter($(self.fc.el.parentNode).find('.originalTimeslot'));
//                        }
//                        else {
//                            preNode = copyTimeSlot.attr('id', result[j].id).insertAfter($(preNode));
//                        }
//                        var clinicDiv = $("<div id="+result[j].id+" class="+ currentClinicDetails + "><strong> "+ result[j].name + "</strong></span>");
//
//                        var dtime_slots = result[j].time_slots
//                        var a ='';
//                        var slot_length = dtime_slots.length
//                        for (var k =0; k < dtime_slots.length; k+=2) {
//                            if(k<4){
//                                a += "<p style='font-size: 12px;margin-bottom:0px;color: darkgreen;font-weight: bold;'>"
//                                if(k<slot_length){
//                                    a += dtime_slots[k].start_hour + ' to ' + dtime_slots[k].end_hour
//                                }
//                                 if(k+1<slot_length){
//                                    a += ', ' + dtime_slots[k+1].start_hour + ' to ' + dtime_slots[k+1].end_hour
//                                }
//                                a += "</p>";
//                            }
//                        }
//                        clinicDiv.append(a)
//
//                        clinicDiv.addClass('displayTimeSlots displayTimeSlotsMargin');
//
//                        var left_css = j*262
//                        copyTimeSlot.css('left',left_css + 'px')
//                        copyTimeSlot.before(clinicDiv);
//                    }
//                }
//
//                $('.displayTimeSlots').css({
//                  'height': divHeight,
//                  "font-size": "16px",
//                  "left": "5",
//                  "text-align": "center",
//                  "color": "darkblue",
//                  "padding-top": "0px",
//                  //"background": "#e6e5e5",
//                  "width": "180px",
//                  "position": "sticky",
//                  "top": "0px",
//                  "z-index": "10",
//                  "margin-top": "-18px",
//                  "margin-bottom": "0px",
//                  "margin-left": "73px",
//                  "margin-right": "2px",
//                });
//
//
//                $.each(gridEvent, function(gride, gridi) {
//                    var splitData = $(gridi).css('inset').split(" ");
//
//                    if (splitData.length >= 4) {
//
//                        $(gridi).css('inset', splitData[0] + ' 0px ' + splitData[2] + ' ' + '95px');
//
//                    }
//                })
//
//                //G.T CODE
//                for (var j =0; j < result.length; j++) {
//                    //  This is used for set the appointment on particular slot of the clinic based on the time
//                    if (j >= 0){
//                        var clinic_id = result[j].id;
//
//                        $.each(gridEvent, async function(gi, ge){
//                            // var self = this;
//                            // var eventName = $(ge).find(".o_event_title")[0].innerText;
//                            var eventName = $(ge).find(".o_event_title")[0].innerText;
//                            await self.rpc('/web/dataset/call_kw/medical.appointment/get_data',{
//                                model: 'medical.appointment',
//                                method: 'get_data',
//                                args: [false, clinic_id, eventName, j],
//                                kwargs: {}//self.context,
//                            })
//                            .then(function(res){
//                                if (res.index >= 1) {
//                                    $(ge).css({
//                                        "padding-top": "0px",
//                                        //"width": "200px",
//                                        "width": "160px",
//                                        "font-weight": "bold",
//                                        "margin-left": res.index * 260 + 'px'
//                                    })
//                                    a = "<p style='font-size: 12px;margin-bottom:0px;font-weight: bold;'>"
//
//                                    if(res.patient){
////                                        $(ge).find(".o_event_title")[0].innerText = " [" + res.clinic + "] " + res.patient + " " + res.service
//                                        $(ge).find(".fc-time")[0].innerText = " [" + res.clinic + "] " + res.patient + " " + res.service
//                                        //ge.appendChild()
//                                    }
//
//                                }
//                                else{
//                                    if(res.patient){
////                                        $(ge).find(".o_event_title")[0].innerText = " [" + res.clinic + "] " + res.patient + " " + res.service
//                                        $(ge).find(".fc-time")[0].innerText = " [" + res.clinic + "] " + res.patient + " " + res.service
//                                    }
//                                }
//                            })
//                        });
//                    }
//                }
//
//                var allDivColumns = $(self.fc.el.parentNode).find('.fc-slats');
//                $.each(allDivColumns, function(ge, gi) {
//                    var clinicID = gi.id;
//                    var divTrList = $(gi).find('table').find('tbody').find('tr');
//                    $.each(divTrList, function(dtl, dtli){
//                        $(dtli).addClass('TimeSlotTD').attr({'id': clinicID});
//                    });
//                });
//
//                // This code is used for remove the except first element if the child is more than one when we increase or decrease the page size
//                //ToDo: Test if it will fix Appointment card visual effect
//                if ($(self.fc.el.parentNode).find('.originalTimeslot').find('div').length >= 1) {
//                    $(self.fc.el.parentNode).find('.originalTimeslot').find('div').slice(1).remove()
//                }
//
//                var real_obj = self.fc.el.parentNode;
//                $(self.fc.el.parentNode).find(".displayTimeSlots").bind("click", {real_obj: self}, self._displayTimeSlots);
//                $(self.fc.el.parentNode).find(".TimeSlotTD").bind("click", {real_obj: self}, self._fcWidgetContent);
//           }
//           else {
//                var find_root_elem = $(self.fc.el.parentNode).find('div.originalTimeslot');
//                console.log(find_root_elem)
//                find_elem.removeAttr('style');
//           }
//        });
//    },
//
////        });
//
//
//})
//
//
//// =====================================FIX BACKGROUND DISPLAY NONE=======================================
//Long Appointment ....................................................................................
/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";

import { RPCError } from '@web/core/network/rpc_service';
import { sprintf } from "@web/core/utils/strings";
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";

import { calendarView } from "@web/views/calendar/calendar_view";
import { CalendarController } from "@web/views/calendar/calendar_controller";
import { CalendarCommonRenderer } from "@web/views/calendar/calendar_common/calendar_common_renderer";
import { CalendarQuickCreate } from "@calendar/views/calendar_form/calendar_quick_create";
import { CalendarCommonPopover } from "@web/views/calendar/calendar_common/calendar_common_popover";
import { CalendarModel } from "@web/views/calendar/calendar_model";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

import { useEffect, useEnv, useSubEnv } from "@odoo/owl";
import { session } from "@web/session";
import { Dialog } from "@web/core/dialog/dialog";
// Used to Refresh the page each period
import { WebClient } from "@web/webclient/webclient";


patch(CalendarCommonPopover.prototype, {
    setup () {
        super.setup();
        // this.canInvoice = false;
        this.canPayment = false;
        this.actionService = useService("action");
        if('is_invoice_state' in this.props.record.rawRecord){
            this.canInvoice = this.props.record.rawRecord.is_invoice_state;
            this.canOrder = this.props.record.rawRecord.is_invoice_state;
        }

        console.log(this, "popover");
        if('invoice_amount' in this.props.record.rawRecord && 'invoice_paid' in this.props.record.rawRecord){
            var invoice_amount = this.props.record.rawRecord.invoice_amount
            var invoice_paid = this.props.record.rawRecord.invoice_paid
            console.log(invoice_amount, invoice_paid, "paid")

            if(invoice_amount == invoice_paid){
                if(invoice_paid > 0){
                    this.canPayment = true;
                }
            }
        }
    },

    _onClickOrderOpen: function (ev) {
        var self = this;
        console.log(ev)
        console.log(self)
        var context = {'default_appointment_id': parseInt(self.props.record.id)};
        self.props.close();
        return self.actionService.doAction({
            name: 'Create: Sale Order',
            type: 'ir.actions.act_window',
            //res_model: 'calender.invoice.wizard',
            res_model: 'calender.sale.wizard',
            target: 'new',
            views: [[false, 'form']],
            context: context,
        });
    },

    _onClickInvoiceOpen: function (ev) {
        var self = this;
        console.log(ev)
        console.log(self)
        var context = {'default_appointment_id': parseInt(self.props.record.id)};
        self.props.close();
        return self.actionService.doAction({
            name: 'Create: Invoices',
            type: 'ir.actions.act_window',
            res_model: 'calender.invoice.wizard',
            target: 'new',
            views: [[false, 'form']],
            context: context,
        });
    },

    _onClickPaymentOpen: function (ev) {
        var self = this;
        var context = {'default_appointment_id': parseInt(self.props.record.id)};
        self.props.close();
        return self.actionService.doAction({
            name: 'Register Payment',
            type: 'ir.actions.act_window',
            res_model: 'calender.payment.wizard',
            target: 'new',
            views: [[false, 'form']],
            context: context,
        });
    },

    _onClickNotesOpen: function (ev) {
        var self = this;
        var context = {'default_appointment_id': parseInt(self.props.record.id)};
        self.props.close();
        return self.actionService.doAction({
            name: 'Create: Notes',
            type: 'ir.actions.act_window',
            res_model: 'calender.notes.wizard',
            target: 'new',
            views: [[false, 'form']],
            context: context,
        });
    },

    _onClickChartOpen: function (ev) {
        ev.preventDefault();
        var self = this;
        var context = {'default_appointment_id': parseInt(self.props.record.id)};
        self.props.close();
        return self.actionService.doAction({
            name: 'Face/Body Chart',
            type: 'ir.actions.client',
            tag: 'face_body_chart',
            target: 'current',
            context: context,
        });
    },

    async get_events() {
        var self = this;
        await this.__owl__.bdom;
        $('.o_popover_container').find('.o_cw_popover_order_m').bind("click", {real_obj: self}, self._onClickOrderOpen)
        $('.o_popover_container').find('.o_cw_popover_invoice_m').bind("click", {real_obj: self}, self._onClickInvoiceOpen)
    },

    dateToServer (date, fieldType) {
        date = date.clone().locale('en');
        if (fieldType === "date") {
            return date.local().format('YYYY-MM-DD');
        }
        return date.utc().format('YYYY-MM-DD HH:mm:ss');
    }


});

    //DONE!

    //========================================================================================
    //========================================================================================

patch(CalendarCommonRenderer.prototype, {
    //DONE!
    setup () {
        super.setup();

        this.rpc = useService("rpc");
        this.actionService = useService("action");
        this.dialogService = useService("dialog");

        // Listen for backend-triggered refresh events

         //this.on_ui_change();
//================THIS TO REFRESH EVERY 10 Second====
//        setInterval(() => {
//            this.loadRecords()
//        }, 10000);//refresh every 10 seconds
//===============================================

            if (this.props.model.meta.resModel && this.props.model.meta.resModel=='medical.appointment'){
                useEffect(() => {
                    this.get_clinics_slot_details();
                    //=================================================================
                    //var $eventTitle = $event.find('.o_event_title.text-truncate');
                    //if ($eventTitle.length) { $eventTitle.removeClass('text-truncate');}
                    // ================================================================
            });
        }
    },

    //    ==================================================================================================
    //    ==================================================================================================

    //    ==================================================================================================
    //    ==================================================================================================

    //DONE!
    _displayTimeSlots: async function (e) {

        var date_time = e.data.real_obj.props.model.data.range.start.toString();
        var t = date_time.split(/[- :]/);
        var date = new Date(date_time);
        var target_date = date.toString();
        //  await this._rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot',{
         await this._rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot',{
            model: 'clinic.slot',
            method: 'get_clinics_slot',
            args: [target_date.split(' (')[0], e.currentTarget.id],
            kwargs: {context: e.data.real_obj.props.model.meta.context}//self.context,
        }).then(function (clinicResult) {
            if (clinicResult) {

                var dtime_slots = clinicResult[0].time_slots
                var doc_name = clinicResult[0].name

                var a ='';
                for (var k =0; k < dtime_slots.length; k++) {
                    a += dtime_slots[k].start_hour + ' to ' + dtime_slots[k].end_hour + " ";
                }
                 e.data.real_obj.dialogService.add(ConfirmationDialog, {
                    body:  a,
                    title:  _t("Time Slots of " + doc_name),
                    confirm: () => {},
                });
            }
        });
    },
    //DONE!
    _fcWidgetContent: async function (ev) {
        // var self = this;
        var date_time = ev.data.real_obj.props.model.data.range.start.toString();
        var t = date_time.split(/[- :]/);
        var date = new Date(date_time);
        var target_date = date.toString();
        var context = {};
        if(ev.currentTarget.id){
            context['default_clinic_id'] = parseInt(ev.currentTarget.id) || false;
        }
        else if(ev.target.id){
            context['default_clinic_id'] = parseInt(ev.target.id) || false;
        }
        context['from_time'] = ev.currentTarget.dataset.time || $(ev.target).parent()[0].dataset.time;
        context['dateToString'] = target_date.split(' (')[0];
        await ev.data.real_obj.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot_validation',{
            model: 'clinic.slot',
            method: 'get_clinics_slot_validation',
            args: [target_date.split(' (')[0], ev.currentTarget.id],
            kwargs: {context: context}
        }).then(function (result) {
            if(result){
                ev.data.real_obj.actionService.doAction({
                    name: 'Create: Appointments',
                    type: 'ir.actions.act_window',
                    res_model: 'calender.appointment.wizard',
                    target: 'new',
                    views: [[false, 'form']],
                    context: context,
                });
            }else{

                var content ='Appointment Slot is not available.';

                ev.data.real_obj.dialogService.add(ConfirmationDialog, {
                    body:  content,
                    title:  _t("Alert"),
                    confirm: () => {},
                });
            }
        })
    },

    async loadRecords(){
        const result = await this.rpc("/web/dataset/call_kw",{
            model: "medical.appointment",
//            method: "get_views",
            method: "search_read",
            args:[[]],
            kwargs: {
                    context: []
                }
        });
        this.state.records = result;
    },
// To Reload calendar records periodically


    async get_clinics_slot_details_rpc(eventName,clinic_id,j) {
        var self = this;

        await self.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot_validation',{
            model: 'medical.appointment',
            method: 'get_data',
            args: [false, clinic_id, eventName, j],
            kwargs: {context: []}
        }).then(function (result) {
        console.log("=============res111=============",result)
        })
    },

    // DONE
    async get_clinics_slot_details(checkResizeWindow) {
        var $containerHeight = $(window).height();
        var self = this;

        var date_time = self.props.model.data.range.start.toString();
        var t = date_time.split(/[- :]/);
        var date = new Date(date_time);
        var target_date = date.toString();

        await this.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot',{
            model: 'clinic.slot',
            method: 'get_clinics_slot',
            args: [target_date.split(' (')[0]],
            kwargs: {context: self.props.model.meta.context}//self.context,
        }).then(function (result) {

            if (result) {
                $(self.fc.el.parentNode).find('.fc-time-grid-container').css({
                    'overflow': 'scroll',
                    'margin-top': '20%',
                    'position': 'relative',
                })
                var rl = result.length * 280;
                if (rl <= 1400) {
                    rl = 1400;
                }
                $(self.fc.el.parentNode).find('.fc-time-grid').addClass("row");
                $(self.fc.el.parentNode).find('.fc-time-grid').css({
                   'width' : rl + 'px',
                   'position': 'relative',
                   'height': '-webkit-fill-available',
                });
                var s = $(self.fc.el.parentNode).find('.fc-slats').slice(1).remove();
                $(self.fc.el.parentNode).find('.fc-slats').addClass("originalTimeslot");
                $(self.fc.el.parentNode).find('.fc-slats').css({'width': '260px','z-index': '0'});
                //G.T CODE
                $(self.fc.el.parentNode).find('.fc-widget-content').css({'margin-top':'-280px'})

                //  This code is used for hide the tr and its td if this operation not perform then
                //  our td click event not work every time
                $(self.fc.el.parentNode).find('.fc-bg').css({
                      'display': 'none',
                    });
                $(document).ready(function() {
                    $('.fc-resizer.fc-end-resizer').next('.fc-bg').css('display', 'block');
                });

                var preNode = false;
                var s = $(self.fc.el.parentNode).find('div.fc-slats');

                // This is used for set the width of appointment create
                //G.T CODE
                var gridEvent = $(self.fc.el.parentNode).find('a.fc-time-grid-event').css({

                    "width": "200px",
                    "font-weight":"bold",
                    "z-index": "1",
                    "padding-top": "0px",
                    "margin-top": 0 + '%',
                    "cursor": "pointer",

                })

                //here fix
                if($(self.fc.el.parentNode).find('a.fc-time-grid-event').length){
                    $.each($(self.fc.el.parentNode).find('a.fc-time-grid-event'), function(e,i){
                        var top_css = $(i).css("top")
                        var top_a = top_css;
                        var top_b = top_a.replace("px", "");
                        var top_c = parseInt(top_b) - 40;
                        var top_d =  top_c.toString() + 'px';
                        $(i).css("top",top_d)

                        var bottom_css = $(i).css("bottom")
                        var bottom_a = bottom_css;
                        var bottom_b = bottom_a.replace("px", "");
                        var bottom_c = parseInt(bottom_b) + 40;
                        var bottom_d =  bottom_c.toString() + 'px';
                        $(i).css("bottom",bottom_d)
                    })
                }

                var divHeight = '20px';
                for (var j =0; j < result.length; j++) {
                    console.log("=================2=============",s)
                    $.each(s, function(e,i){
                        var trList = $(i).find('table').find('tbody').find('tr');
                        var trFirst = $(i).find('table').find('tbody').find('tr:eq(0)');
                        var trSecond = $(i).find('table').find('tbody').find('tr:eq(1)');
                        divHeight = trFirst.height() + trSecond.height() + 20 + 'px';
                        trFirst.css({'display': 'none'});
                        trSecond.css({'display': 'none'});
                    })
                }
                $('.displayTimeSlots').addClass('d-none')
                for (var j =0; j < result.length; j++) {
                    if (j == 0) {

                        var clinicName = result[j].name;
                        $(self.fc.el.parentNode).find('.fc-slats').attr('id', result[j].id);
                        var clinicDetails = 'clinicDetails_' + j + '_' + result[j].id;
                        var newDynamicClass = 'mypopshow_' + j + '_' + result[j].id;
                        var clinicDiv = $("<div id="+result[j].id+" class=" + clinicDetails +"><strong style='margin-bottom:0px'> "+ result[j].name +
                        "</strong></span>");

                        var dtime_slots = result[j].time_slots
                        var a ='';
                        var slot_length = dtime_slots.length
                        for (var k =0; k < dtime_slots.length; k+=2) {
                            if(k<4){
                                a += "<p style='font-size: 12px;margin-bottom:0px;color: darkgreen;font-weight: bold;'>"
                                if(k<slot_length){
                                    a += dtime_slots[k].start_hour + ' to ' + dtime_slots[k].end_hour
                                }

                                 if(k+1<slot_length){
                                    a += ', ' + dtime_slots[k+1].start_hour + ' to ' + dtime_slots[k+1].end_hour
                                }
                                a += "</p>";
                            }
                        }

                        clinicDiv.append(a)
                        clinicDiv.addClass('displayTimeSlots');

                        $(self.fc.el.parentNode).find('.fc-slats').before(clinicDiv);
                    }
                    else {
                        var copyTimeSlot = $('.originalTimeslot').clone();
                        copyTimeSlot.removeClass("originalTimeslot");
                        var clinicName = result[j].name;
                        var clinicDetails = 'clinicDetails_0_' + result[0].id;
                        var currentClinicDetails = 'clinicDetails_' + j + '_' + result[j].id;

                        copyTimeSlot.find('div.' + clinicDetails).remove()
                        if (!preNode) {
                            preNode = copyTimeSlot.attr('id', result[j].id).insertAfter($(self.fc.el.parentNode).find('.originalTimeslot'));
                        }
                        else {
                            preNode = copyTimeSlot.attr('id', result[j].id).insertAfter($(preNode));
                        }
                        var clinicDiv = $("<div id="+result[j].id+" class="+ currentClinicDetails + "><strong> "+ result[j].name + "</strong></span>");

                        var dtime_slots = result[j].time_slots
                        var a ='';
                        var slot_length = dtime_slots.length
                        for (var k =0; k < dtime_slots.length; k+=2) {
                            if(k<4){
                                a += "<p style='font-size: 12px;margin-bottom:0px;color: darkgreen;font-weight: bold;'>"
                                if(k<slot_length){
                                    a += dtime_slots[k].start_hour + ' to ' + dtime_slots[k].end_hour
                                }
                                 if(k+1<slot_length){
                                    a += ', ' + dtime_slots[k+1].start_hour + ' to ' + dtime_slots[k+1].end_hour
                                }
                                a += "</p>";
                            }
                        }
                        clinicDiv.append(a)

                        clinicDiv.addClass('displayTimeSlots displayTimeSlotsMargin');

                        var left_css = j*262
                        copyTimeSlot.css('left',left_css + 'px')
                        copyTimeSlot.before(clinicDiv);
                    }
                }

                $('.displayTimeSlots').css({
                  'height': divHeight,
                  "font-size": "16px",
                  "left": "5",
                  "text-align": "center",
                  "color": "darkblue",
                  "padding-top": "0px",
                  //"background": "#e6e5e5",
                  "width": "180px",
                  "position": "sticky",
                  "top": "0px",
                  "z-index": "10",
                  "margin-top": "-18px",
                  "margin-bottom": "0px",
                  "margin-left": "73px",
                  "margin-right": "2px",
                });


                $.each(gridEvent, function(gride, gridi) {
                    var splitData = $(gridi).css('inset').split(" ");

                    if (splitData.length >= 4) {

                        $(gridi).css('inset', splitData[0] + ' 0px ' + splitData[2] + ' ' + '95px');

                    }
                })

                //G.T CODE
                for (var j =0; j < result.length; j++) {
                    //  This is used for set the appointment on particular slot of the clinic based on the time
                    if (j >= 0){
                        var clinic_id = result[j].id;

                        $.each(gridEvent, async function(gi, ge){
                            // var eventName = $(ge).find(".o_event_title")[0].innerText;
                            var eventName = $(ge).find(".o_event_title")[0].innerText;
                            await self.rpc('/web/dataset/call_kw/medical.appointment/get_data',{
                                model: 'medical.appointment',
                                method: 'get_data',
                                args: [false, clinic_id, eventName, j],
                                kwargs: {}//self.context,
                            })
                            .then(function(res){
                                if (res.index >= 1) {
                                    $(ge).css({
                                        "padding-top": "0px",
                                        "width": "200px",
                                        "font-weight": "bold",
                                        "margin-left": res.index * 260 + 'px'
                                    })
                                    a = "<p style='font-size: 12px;margin-bottom:0px;font-weight: bold;'>"

                                    if(res.patient){
//                                        $(ge).find(".o_event_title")[0].innerText = " [" + res.clinic + "] " + res.patient + " " + res.service
                                        $(ge).find(".fc-time")[0].innerText = " [" + res.clinic + "] " + res.patient + " " + res.service
                                        //ge.appendChild()
                                    }

                                }
                                else{
                                    if(res.patient){
//                                        $(ge).find(".o_event_title")[0].innerText = " [" + res.clinic + "] " + res.patient + " " + res.service
                                        $(ge).find(".fc-time")[0].innerText = " [" + res.clinic + "] " + res.patient + " " + res.service
                                    }
                                }
                            })
                        });
                    }
                }

                var allDivColumns = $(self.fc.el.parentNode).find('.fc-slats');
                $.each(allDivColumns, function(ge, gi) {
                    var clinicID = gi.id;
                    var divTrList = $(gi).find('table').find('tbody').find('tr');
                    $.each(divTrList, function(dtl, dtli){
                        $(dtli).addClass('TimeSlotTD').attr({'id': clinicID});
                    });
                });

                // This code is used for remove the except first element if the child is more than one when we increase or decrease the page size
                //ToDo: Test if it will fix Appointment card visual effect
                if ($(self.fc.el.parentNode).find('.originalTimeslot').find('div').length >= 1) {
                    $(self.fc.el.parentNode).find('.originalTimeslot').find('div').slice(1).remove()
                }

                var real_obj = self.fc.el.parentNode;
                $(self.fc.el.parentNode).find(".displayTimeSlots").bind("click", {real_obj: self}, self._displayTimeSlots);
                $(self.fc.el.parentNode).find(".TimeSlotTD").bind("click", {real_obj: self}, self._fcWidgetContent);
           }
           else {
                var find_root_elem = $(self.fc.el.parentNode).find('div.originalTimeslot');
                console.log(find_root_elem)
                find_elem.removeAttr('style');
           }
        });
    },

//        });


})
