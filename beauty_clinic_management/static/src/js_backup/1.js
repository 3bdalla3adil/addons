/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { CalendarController } from "@web/views/calendar/calendar_controller";
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { CalendarCommonRenderer } from "@web/views/calendar/calendar_common/calendar_common_renderer";
import { CalendarQuickCreate } from "@calendar/views/calendar_form/calendar_quick_create";
console.log("========AttendeeCalendarController====CUSTOM 17==",patch)
import { useEffect } from "@odoo/owl";
import { session } from "@web/session";

patch(CalendarCommonRenderer.prototype, {

    setup () {
        super.setup();

        this.rpc = useService("rpc");
        this.actionService = useService("action");
        console.log("========CALANDER INHERIT====CUSTOM NEW==",this)
            if (this.props.model.meta.resModel && this.props.model.meta.resModel=='medical.appointment'){
                useEffect(() => {
                this.get_clinics_slot_details();
            });
        }

    },


    _displayTimeSlots: function (e) {
        // var self = this;
        var date_time = e.data.real_obj.props.model.data.range.start.toString();
        var t = date_time.split(/[- :]/);
        var date = new Date(date_time);
        var target_date = date.toString();

        this.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot',{
            model: 'clinic.slot',
            method: 'get_clinics_slot',
            args: [target_date.split(' (')[0], e.currentTarget.id],
            kwargs: {context: e.data.real_obj.props.model.meta.context}//self.context,
        }).then(function (clinicResult) {
            if (clinicResult) {

                var dtime_slots = clinicResult[0].time_slots
                var a ='<html><body><div>';
                for (var k =0; k < dtime_slots.length; k++) {
                    a += "<span style='margin-left: 25px;display: flex'>" + dtime_slots[k].start_hour + ' to ' + dtime_slots[k].end_hour + "</span>";
                }
                a += "</div></body></html>"
                console.log(Dialog);
                Dialog.alert(e.data.real_obj, '', {
                    title: _t("Time Slots of " + e.target.innerText),
                    $content: a
                });
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
            context['default_clinic_id'] = parseInt(ev.currentTarget.id) || false;
        }
        else if(ev.target.id){
            context['default_clinic_id'] = parseInt(ev.target.id) || false;
        }
        context['from_time'] = ev.currentTarget.dataset.time || $(ev.target).parent()[0].dataset.time;
        context['dateToString'] = target_date.split(' (')[0];
        await this.rpc('/web/dataset/call_kw/clinic.slot/get_clinics_slot_validation',{
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
                var content ='<html><body><div>';
                content += "<span style='margin-left: 25px;display: flex'>Appointment Slot is not available.</span>";
                content += "</div></body></html>"
                Dialog.alert(ev.data.real_obj, '', {
                    title: _t("Alert"),
                    $content: content,
                });
            }
        })

    },

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
                    'overflow': 'auto',

                    'position': 'relative',
                })
                var rl = result.length * 280;
                if (rl <= 1400) {
                    rl = 1400;
                }
                $(self.fc.el.parentNode).find('.fc-time-grid').addClass("row");
                $(self.fc.el.parentNode).find('.fc-time-grid').css({
                   'width' : rl + 'px',
                   'overflow': 'auto',
                   'position': 'relative',
                   'height': '-webkit-fill-available',
                });
                var s = $(self.fc.el.parentNode).find('.fc-slats').slice(1).remove();
                $(self.fc.el.parentNode).find('.fc-slats').addClass("originalTimeslot");
                $(self.fc.el.parentNode).find('.fc-slats').css({'width': '260px'});

                //  This code is used for hide the tr and its td if this operation not perform then
                //  our td click event not work every time
                $(self.fc.el.parentNode).find('.fc-bg').css({
                      'display': 'none'
                    });

                var preNode = false;
                var s = $(self.fc.el.parentNode).find('div.fc-slats');

                // This is used for set the width of appointment create
                var gridEvent = $(self.fc.el.parentNode).find('a.fc-time-grid-event').css({
                    "width": "100px",
                    "padding-top": "0px",
                    "margin-top": 0 + '%',
                    "background-color": "lightpink",


                })


                if($(self.fc.el.parentNode).find('a.fc-time-grid-event').length){
                    this.each($(self.fc.el.parentNode).find('a.fc-time-grid-event'), function(e,i){
                        var top_css = $(e).css("top")
                        var top_a = top_css;
                        var top_b = top_a.replace("px", "");
                        var top_c = parseInt(top_b) - 40;
                        var top_d =  top_c.toString() + 'px';
                        $(e).css("top",top_d)

                        var bottom_css = $(e).css("bottom")
                        var bottom_a = bottom_css;
                        var bottom_b = bottom_a.replace("px", "");
                        var bottom_c = parseInt(bottom_b) + 40;
                        var bottom_d =  bottom_c.toString() + 'px';
                        $(e).css("bottom",bottom_d)
                    })
                }

                var divHeight = '20px';
                for (var j =0; j < result.length; j++) {
                    this.each(s, function(e,i){
                        var trList = $(e).find('table').find('tbody').find('tr');
                        var trFirst = $(e).find('table').find('tbody').find('tr:eq(0)');
                        var trSecond = $(e).find('table').find('tbody').find('tr:eq(1)');
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
                  "background": "#e6e5e5",
                  "width": "180px",
                  "position": "sticky",
                  "top": "0px",
                  "z-index": "10",
                  "margin-top": "-18px",
                  "margin-bottom": "0px",
                  "margin-left": "73px",
                  "margin-right": "2px",
                });



                this.each(gridEvent, function(gride, gridi) {
                    var splitData = $(gride).css('inset').split(" ");

                    if (splitData.length >= 4) {

                        console.log("=============splitData=======111==0======",splitData[0] )
                        $(gride).css('inset', splitData[0] + ' 0px ' + splitData[2] + ' ' + '95px');

                    }
                })

                for (var j =0; j < result.length; j++) {
                //  This is used for set the appointment on particular slot of the clinic based on the time
                    if (j >= 0){
                        var clinic_id = result[j].id;
                        console.log("==============result========clinic_idclinic_idclinic_id=result=========",result[j] , clinic_id)
                        this.each(gridEvent, function(ge, gi){
                            var eventName = $(ge).find(".o_event_title")[0].innerText;
                            rpc.query({
                                model: 'medical.appointment',
                                method: 'get_data',
                                args: [false, clinic_id, eventName, j]
                            }).then(function(res){
                                console.log("==============res==res=======",res.index , res.patient , eventName)
                                if (res.index >= 1) {
                                    $(ge).css({
                                        "padding-top": "0px",
                                        "width": "90px",
                                        "background-color": "lightpink",
                                        "margin-left": res.index * 260 + 'px',

                                    })
                                    if(res.patient){
                                        $(ge).find(".o_event_title")[0].innerText = res.patient
                                        console.log('===================patientttttttttttt===' , res.patient , $(ge).find(".o_event_title")[0].innerText , clinic_id)
                                    }

                                }
                                else{
                                    if(res.patient){
                                        $(ge).find(".o_event_title")[0].innerText = res.patient
                                    }
                                }
                            })

                        });

                    }
                }

                var allDivColumns = $(self.fc.el.parentNode).find('.fc-slats');
                this.each(allDivColumns, function(ge, gi) {
                    var clinicID = ge.id;
                    var divTrList = $(ge).find('table').find('tbody').find('tr');
                     this.each(divTrList, function(dtl, dtli){
                        $(dtl).addClass('TimeSlotTD').attr({'id': clinicID});

                     });
                });

                // This code is used for remove the except first element if the child is more than one when we increase or decrease the page size
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
    }

})
//export class BautyCalendarController extends CalendarController {
//    setup() {
//        console.log("========CALANDER INHERIT====CUSTOM 17==")
//        super.setup();
//
//    }
//}