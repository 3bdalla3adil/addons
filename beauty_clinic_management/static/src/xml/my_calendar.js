/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { CalendarController } from "@web/views/calendar/calendar_controller";
import { RPCError } from '@web/core/network/rpc_service';
import { sprintf } from "@web/core/utils/strings";
import { calendarView } from "@web/views/calendar/calendar_view";
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { CalendarCommonRenderer } from "@web/views/calendar/calendar_common/calendar_common_renderer";
import { CalendarQuickCreate } from "@calendar/views/calendar_form/calendar_quick_create";
import { CalendarCommonPopover } from "@web/views/calendar/calendar_common/calendar_common_popover";
import { CalendarModel } from "@web/views/calendar/calendar_model";
console.log("========AttendeeCalendarController====CUSTOM 17==",patch)
import { useEffect, useEnv, useSubEnv } from "@odoo/owl";
import { session } from "@web/session";
import { Dialog } from "@web/core/dialog/dialog";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(CalendarCommonPopover.prototype, {
    setup () {
        super.setup();
        // this.canInvoice = false;
        this.canPayment = false;
        this.actionService = useService("action");
        if('is_invoice_state' in this.props.record.rawRecord){
            this.canInvoice = this.props.record.rawRecord.is_invoice_state;
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
        // this.get_events();

        // this.isEventDeletable = false;
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

//========================================================================================
//========================================================================================

//ToDo: Migrate to Owl Class Based Code
//export class CalendarCommonRenderer extends Component {
//    setup() {

patch(CalendarCommonRenderer.prototype, {

    setup () {
        super.setup();

        this.rpc = useService("rpc");
        this.actionService = useService("action");
        this.dialogService = useService("dialog");

        //        var fcWidgetContentElements = document.querySelectorAll('.fc-widget-content');
        //        for (var element of fcWidgetContentElements) {
        //          element.style.margin = '-288%';
        //          console.log("=====================================ABCD==================================================")
        //        }
        console.log("========CALANDER INHERIT====CUSTOM NEW==",this)
            if (this.props.model.meta.resModel && this.props.model.meta.resModel=='medical.appointment'){
                useEffect(() => {
        //                this.get_clinics_slot_details();
                this.get_clinics_slot_details();
            });
        }
    },


//    async _displayTimeSlots(e) {
    _displayTimeSlots: async function (e) {
        // var self = this;
//        console.log("===update========RPC======1=====",this)
        console.log("===update========RPC======e=====",e)
        console.log("=================================_displayTimeSlots===============================")
//        console.log("===update========RPC======e.data.real_obj=====",e.data.real_obj)
//        var date_time = this.props.model.data.range.start.toString();
        var date_time = e.data.real_obj.props.model.data.range.start.toString();
        var t = date_time.split(/[- :]/);
        var date = new Date(date_time);
        var target_date = date.toString();

//        console.log("===update========target_date======e.target=====",e.target)
//        console.log("===update========target_date=====e.currentTarget=====",e.currentTarget)
//        console.log("===update========target_date======e.currentTarget.id=====",e.currentTarget.id)

//         this.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot',{
         await this._rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot',{
//            model: 'clinic.slot',
            model: 'clinic.slot',
//            method: 'get_clinics_slot',
            method: 'get_clinics_slot',
            args: [target_date.split(' (')[0], e.currentTarget.id],
            kwargs: {context: e.data.real_obj.props.model.meta.context}//self.context,
        }).then(function (clinicResult) {
//            console.log("=============clinicResult===========",clinicResult)
            if (clinicResult) {

                var dtime_slots = clinicResult[0].time_slots
                var clinic_name = clinicResult[0].name
//                var a ='<html><body><div>';
//                for (var k =0; k < dtime_slots.length; k++) {
//                    a += "<span style='margin-left: 25px;display: flex'>" + dtime_slots[k].start_hour + ' to ' + dtime_slots[k].end_hour + "</span>";
//                }
//                a += "</div></body></html>"
                var a ='';
                for (var k =0; k < dtime_slots.length; k++) {
                    a += dtime_slots[k].start_hour + ' to ' + dtime_slots[k].end_hour + " ";
                }
                console.log("=============clinic===========",clinic_name)
                console.log("=============slot===========",a)
//                console.log(Dialog);

                 e.data.real_obj.dialogService.add(ConfirmationDialog, {
                    body:  a,
                    title:  _t("Time Slots of " + clinic_name),
                    confirm: () => {},
                });

//                Dialog.alert(e.data.real_obj, '', {
//                    title: _t("Time Slots of " + e.target.innerText),
//                    $content: a
//                });
            }
        });
    },


    _fcWidgetContent: async function (ev) {
        // var self = this;
        var date_time = ev.data.real_obj.props.model.data.range.start.toString();
        var t = date_time.split(/[- :]/);
        var date = new Date(date_time);
        var target_date = date.toString();
        var context = {};
        if(ev.currentTarget.id){
            //            context['default_clinic_id'] = parseInt(ev.currentTarget.id) || false;
            context['default_clinic_id'] = parseInt(ev.currentTarget.id) || false;
        }
        else if(ev.target.id){
            context['default_clinic_id'] = parseInt(ev.target.id) || false;
        }
        context['from_time'] = ev.currentTarget.dataset.time || $(ev.target).parent()[0].dataset.time;
        context['dateToString'] = target_date.split(' (')[0];
        console.log("===========RPC======2=====",ev.data.real_obj.rpc)
        //DONE!
        //        await this.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot_validation',{
        await ev.data.real_obj.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot_validation',{
            model: 'clinic.slot',
            method: 'get_clinics_slot_validation',
            args: [target_date.split(' (')[0], ev.currentTarget.id],
            kwargs: {context: context}
        }).then(function (result) {
            console.log("===========result======result=====",result)
            if(result){
        //                ev.data.real_obj.actionService.doAction({
                ev.data.real_obj.actionService.doAction({
                    name: 'Create: Appointments',
                    type: 'ir.actions.act_window',
                    res_model: 'calender.appointment.wizard',
                    target: 'new',
                    views: [[false, 'form']],
                    context: context,
                });
            }else{
//                var content ='<html><body><div>';
//                content += "<span style='margin-left: 25px;display: flex'>Appointment Slot is not available.</span>";
//                content += "</div></body></html>"

                var content ='Appointment Slot is not available.';

                ev.data.real_obj.dialogService.add(ConfirmationDialog, {
                    body:  content,
                    title:  _t("Alert"),
                    confirm: () => {},
                });
//                Dialog.alert(ev.data.real_obj, '', {
//                    title: _t("Alert"),
//                    $content: content,
//                });
            }
        })

    },
    //DONE!

    async get_clinics_slot_details_rpc(eventName,clinic_id,j) {
        var self = this;
        console.log("========get_clinics_slot_details_rpc=======eventName==",eventName)
        console.log("========get_clinics_slot_details_rpc=======clinic_id==",clinic_id)
        console.log("========get_clinics_slot_details_rpc=======j==",j)


        await self.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot_validation',{
            model: 'medical.appointment',
            method: 'get_data',
            args: [false, clinic_id, eventName, j],
            kwargs: {context: []}
        }).then(function (result) {
        console.log("=============res111=============",result)
        })
    },

//    async get_clinics_slot_details(checkResizeWindow) {
    async get_clinics_slot_details(checkResizeWindow) {
        var $containerHeight = $(window).height();
        var self = this;
        console.log(this);
        console.log(self);
        // var target_date = self.props.range.target_date.toString();
        var date_time = self.props.model.data.range.start.toString();
        var t = date_time.split(/[- :]/);
        var date = new Date(date_time);
        var target_date = date.toString();
        console.log(target_date.split(' (')[0]);
        console.log(date_time);
//        await this.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot',{
        await this.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot',{
            model: 'clinic.slot',
            method: 'get_clinics_slot',
            args: [target_date.split(' (')[0]],
            kwargs: {context: self.props.model.meta.context}//self.context,
        }).then(function (result) {

            if (result) {
                console.log("==========result+++1111111111111+++++++++++++===========",result,"oioiooi",self.fc.el.parentNode)
                // console.log(self.fc.el.querySelector('.fc-time-grid-container'))
                $(self.fc.el.parentNode).find('.fc-time-grid-container').css({
                //  'overflow': 'auto',
                    'margin-top': '20%', //To Reveal Clinic and Time Slot

                    'position': 'relative',
                })
                var rl = result.length * 280;
                if (rl <= 1400) {
                    rl = 1400;
                }
                $(self.fc.el.parentNode).find('.fc-time-grid').addClass("row");
                $(self.fc.el.parentNode).find('.fc-time-grid').css({
                   'width' : rl + 'px',
                   // 'overflow': 'auto',
                   'position': 'relative',
                   'height': '-webkit-fill-available',
                });
                var s = $(self.fc.el.parentNode).find('.fc-slats').slice(1).remove();
                $(self.fc.el.parentNode).find('.fc-slats').addClass("originalTimeslot");
                $(self.fc.el.parentNode).find('.fc-slats').css({'width': '260px','z-index': '0'});
                //G.T CODE
                $(self.fc.el.parentNode).find('.fc-widget-content').css({'margin-top':'-280px'})
    //                $(self.fc.el.parentNode).find('.fc-slats').css({'width': '260px','z-index': '1'});

                //  This code is used for hide the tr and its td if this operation not perform then
                //  our td click event not work every time
                $(self.fc.el.parentNode).find('.fc-bg').css({
                    'display': 'none'
                    });

                $(document).ready(function() {
                    $('.fc-resizer.fc-end-resizer').next('.fc-bg').css('display', 'block');
                });

                var preNode = false;
                var s = $(self.fc.el.parentNode).find('div.fc-slats');

                // This is used for set the width of appointment create
                //G.T CODE
                var gridEvent = $(self.fc.el.parentNode).find('a.fc-time-grid-event').css({
                    "width": "7%",
                    //"height": "20px",
                    "z-index": "1",
                    "padding-top": "0px",
                    "margin-top": 0 + '%',
                    //"background-color": "lightpink",
                    "cursor": "pointer",

                })
                console.log("=================gridEvent=============",gridEvent)

                //here fix
                if($(self.fc.el.parentNode).find('a.fc-time-grid-event').length){
                    console.log("=================1=============",$(self.fc.el.parentNode).find('a.fc-time-grid-event'))
                    $.each($(self.fc.el.parentNode).find('a.fc-time-grid-event'), function(e,i){
                        console.log("=================top_eeeee=============",e)
                        console.log("=================top_iiiii=============",i)
                        var top_css = $(i).css("top")
                        var top_a = top_css;
                        console.log("=================top_a=============",top_a)
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
                        // $(i).addClass('fc-draggable');
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
                        console.log('===+++++++=======clinicName==clinicName===========' ,clinicName )
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
                                // a += "<p style='font-size: 10px;margin-bottom:0px'>" + dtime_slots[k].start_hour + ' to ' + dtime_slots[k].end_hour + "</p>";
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
                        console.log("==========clinicDiv=======SECOND=====",clinicDiv)

                        $(self.fc.el.parentNode).find('.fc-slats').before(clinicDiv);
                    }
                    else {
                        var copyTimeSlot = $('.originalTimeslot').clone();
                        copyTimeSlot.removeClass("originalTimeslot");
                        var clinicName = result[j].name;
                        var clinicDetails = 'clinicDetails_0_' + result[0].id;
                        var currentclinicDetails = 'clinicDetails_' + j + '_' + result[j].id;

                        copyTimeSlot.find('div.' + clinicDetails).remove()
                        if (!preNode) {
                            preNode = copyTimeSlot.attr('id', result[j].id).insertAfter($(self.fc.el.parentNode).find('.originalTimeslot'));
                        }
                        else {
                            preNode = copyTimeSlot.attr('id', result[j].id).insertAfter($(preNode));
                        }
                        var clinicDiv = $("<div id="+result[j].id+" class="+ currentclinicDetails + "><strong> "+ result[j].name + "</strong></span>");

                        var dtime_slots = result[j].time_slots
                        var a ='';
                        var slot_length = dtime_slots.length
                        for (var k =0; k < dtime_slots.length; k+=2) {
                            if(k<4){
                                // a += "<p style='font-size: 10px;margin-bottom:0px'>" + dtime_slots[k].start_hour + ' to ' + dtime_slots[k].end_hour + "</p>";
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


                console.log("=================3=============", result.length)
                $.each(gridEvent, function(gride, gridi) {
                    var splitData = $(gridi).css('inset').split(" ");

                    if (splitData.length >= 4) {

                        console.log("=============splitData=======111==0======",splitData[0] )
                        $(gridi).css('inset', splitData[0] + ' 0px ' + splitData[2] + ' ' + '95px');

                    }
                })

                //G.T CODE
                for (var j =0; j < result.length; j++) {
                //  This is used for set the appointment on particular slot of the clinic based on the time
                    if (j >= 0){
                        var clinic_id = result[j].id;
                        console.log("=======4=======result========clinic_id=========",result[j] , clinic_id)
    //                        console.log("=============gridEvent=============",gridEvent)

                        $.each(gridEvent, async function(gi, ge){
                            var eventName = $(ge).find(".o_event_title")[0].innerText;
                            console.log("=============self.rpc=============",eventName)
                            console.log("=============clinic_id===========",clinic_id)
                            console.log("=============j=============",j)
                            console.log("=============eventName=============",eventName)
                            await self.rpc('/web/dataset/call_kw/medical.appointment/get_data',{
                                model: 'medical.appointment',
                                method: 'get_data',
//                                args: [false, clinic_id, eventName, j],
                                args: [false, clinic_id, eventName, j],
                                kwargs: {}//self.context,
                            })
                            .then(function(res){

    //                                    console.log("==============res=========",res)
                                if (res.index >= 1) {
                                    $(ge).css({
                                        "padding-top": "0px",
                                        "width": "90px",
                                        "background-color": "lightpink",
                                        "margin-left": res.index * 260 + 'px'
                                    })
                                    if(res.patient){
                                    //    $(ge).find(".o_event_title")[0].innerText = res.patient
                                        $(ge).find(".o_event_title")[0].innerText = '['+res.patient_id+'] ' + res.patient
                                    }

                                }
                                else{
                                    if(res.patient){
                                    //    $(ge).find(".o_event_title")[0].innerText = res.patient
                                        $(ge).find(".o_event_title")[0].innerText = '['+res.patient_id+'] ' + res.patient
                                    }
                                }
                            })

                        });




                    }
                }

                var allDivColumns = $(self.fc.el.parentNode).find('.fc-slats');
    //                console.log("===========allDivColumns============",allDivColumns)
                $.each(allDivColumns, function(ge, gi) {
                    var clinicID = gi.id;
    //                    var clinicID = ge.id;
    //                    console.log("===========gi============",gi)
    //                    console.log("===========clinicID============",clinicID)
                        var divTrList = $(gi).find('table').find('tbody').find('tr');
    //                    console.log("===========divTrList============",divTrList)
                         $.each(divTrList, function(dtl, dtli){
    //                        console.log("===========dtl============",dtli)
                        $(dtli).addClass('TimeSlotTD').attr({'id': clinicID});

                     });
                });

                // This code is used for remove the except first element if the child is more than one when we increase or decrease the page size
                if ($(self.fc.el.parentNode).find('.originalTimeslot').find('div').length >= 1) {
                    $(self.fc.el.parentNode).find('.originalTimeslot').find('div').slice(1).remove()
                }
                var real_obj = self.fc.el.parentNode;
    //                console.log("===========allDivColumns=====2=======",real_obj)

    //                var self = this;  // Assuming you have a reference to the current context

                    // Find the parent element of self.fc.el and bind the click event
    //                var parentElement = self.fc.el.parentNode;
    //                var displayTimeSlotsElement = parentElement.querySelector(".displayTimeSlots");
    //
    //                displayTimeSlotsElement.addEventListener("click", function (event) {
    //                    console.log("============displayTimeSlotsElement=========displayTimeSlotsElement=====",self)
    //                    self._displayTimeSlots(event);
    //                });


                $(self.fc.el.parentNode).find(".displayTimeSlots").bind("click", {real_obj: self}, self._displayTimeSlots);
                $(self.fc.el.parentNode).find(".TimeSlotTD").bind("click", {real_obj: self}, self._fcWidgetContent);
           }
           else {
                var find_root_elem = $(self.fc.el.parentNode).find('div.originalTimeslot');
                console.log(find_root_elem)
                find_elem.removeAttr('style');
           }
        });
    }


})

// =====================================FIX BACKGROUND DISPLAY NONE=======================================

