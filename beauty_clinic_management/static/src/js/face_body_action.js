/** @odoo-module **/

import { Component, onWillStart, useRef, useState, useExternalListener } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useBus, useService } from "@web/core/utils/hooks";
import { url } from "@web/core/utils/urls";

export class FaceBodyChart extends Component {

    setup() {
        this.actionService = useService("action");
        this.companyService = useService("company");
        this.notification = useService("notification");
        this.rpc = useService("rpc");
        this.orm = useService("orm");
        this.is_edit = true;
        this.state = useState({
            is_edit: true,
            is_edit_body: true,
        });
        this.faceRef = useRef("face");
        this.faceBodyRef = useRef("faceBody");
        this.lastX = 0;
        this.lastY = 0;
        this.lastXBody = 0;
        this.lastYBody = 0;
        this.single_mark = [];
        this.multi_mark = [];
        this.mousePressed = false;
        this.mousePressedBody = false;
        this.single_mark_body = [];
        this.multi_mark_body = [];
        this.delete_ids = [];
        this.delete_body_ids = [];
        this.products = false;
        this.appointment_id = this.props.action.context.default_appointment_id || false;
        onWillStart(async () => {
            const locationId = await this.rpc("/web/dataset/call_kw/product.product/search_read", {
                model: 'product.product',
                method: 'search_read',
                args: [],
                kwargs: {domain: [['is_material', '=', true]], fields: ['name']},
            });
            console.log("=======locationId", locationId)
            // this.updateLocationId(locationId);
            this.products = locationId;
        });
        console.log("==========this==========", this);
        // this.ctxBody = self.$el.find("#myCanvasBody")[0].getContext("2d");
        
        // useExternalListener(this.faceRef, "mousedown", this.onMouseDownMyCanvas, true);
    }

    _calculationSubtotal(ev) {
        var qauntity = $(ev.currentTarget).closest("tr").find('td input[name="quantity"]').val()
        var unit_price = $(ev.currentTarget).closest("tr").find('td input[name="unit_price"]').val()
        if (qauntity && unit_price) {
            $(ev.currentTarget).closest("tr").find('td input[name="subtotal"]').val(parseInt(qauntity) * parseInt(unit_price))
        }
        var total = 0
        $('#faceMaterialTable tbody tr').each(function() {
            var subtotal = parseInt($(this).find('td input[name="subtotal"]').val())
            total += subtotal
        })
        console.log("=====_calculationSubtotal========", $('#faceTotal'))
        console.log("=====_calculationSubtotal========", total)
        if (total) {
            $('#faceTotal').html(total)
        }else{
            $('#faceTotal').html(0)
        }
    }

    _calculationSubtotalBody(ev) {
        var qauntity = $(ev.currentTarget).closest("tr").find('td input[name="quantity"]').val()
        var unit_price = $(ev.currentTarget).closest("tr").find('td input[name="unit_price"]').val()
        if (qauntity && unit_price) {
            $(ev.currentTarget).closest("tr").find('td input[name="subtotal"]').val(parseInt(qauntity) * parseInt(unit_price))
        }
        var total = 0
        $('#bodyMaterialTable tbody tr').each(function() {
            var subtotal = parseInt($(this).find('td input[name="subtotal"]').val())
            total += subtotal
        })
        console.log("=====_calculationSubtotal========", $('#faceTotal'))
        console.log("=====_calculationSubtotal========", total)
        if (total) {
            $('#bodyTotal').html(total)
        }else{
            $('#bodyTotal').html(0)
        }
    }

    // Main Face Top Button
    onClickFaceBtn(e) {
        var ctx = $(this.faceRef.el)[0].getContext("2d");
        var self = this;
        $('.globle_btn').removeClass('btn-primary text-white')
        $('.globle_btn').addClass('btn-secondary')
        $('#faceBtn').removeClass('btn-secondary')
        $('#faceBtn').addClass('btn-primary text-white')

        $('.globleImage').addClass('d-none')
        $('#myCanvas').removeClass('d-none')
        $('#myCanvasBtns').removeClass('d-none')
        $('#myCanvasContent').removeClass('d-none')
        // self.rpc("/web/dataset/call_kw/product.product/search_read", {
        //     model: 'product.product',
        //     method: 'search_read',
        //     args: [],
        //     domain: [
        //         ['is_material', '=', true],
        //     ],
        //     kwargs: {},
        // }).then(function(resp) {
        //     console.log("========MATERIAL PRODUCTS===========", resp)
        //     self.products = resp
        // });
        // console.log("=========products=========", self.products);
        if (this.appointment_id) {
            // For Getting Face Chart Marker
            self.rpc("/web/dataset/call_kw/medical.markers.history/search_read",{
                model: 'medical.markers.history',
                method: 'search_read',
                args: [],
                kwargs: {domain: [
                    ['appointment_id', '=', parseInt(this.appointment_id)],
                ],},
            }).then(function(data) {
                for (var k = 0; k < data.length; k++) {
                    var strCoordinate = data[k]['name']
                    var singleArray = strCoordinate.replace(/'/g, '"');
                    var dataCoor = JSON.parse(singleArray)
                    if (dataCoor) {
                        for (var i = 0; i < dataCoor.length; i++) {
                            var sub_data = dataCoor[i]
                            ctx.beginPath();
                            ctx.strokeStyle = 'black';
                            ctx.lineWidth = 6;
                            ctx.lineJoin = "round";
                            ctx.moveTo(sub_data[0], sub_data[1]);
                            ctx.lineTo(sub_data[2], sub_data[3]);
                            ctx.closePath();
                            ctx.stroke();
                        }
                    }
                }
            })

            // For Getting Main Appointment
            self.rpc("/web/dataset/call_kw/medical.appointment/search_read",{
                model: 'medical.appointment',
                method: 'search_read',
                args: [],
                domain: [
                    ['id', '=', parseInt(self.appointment_id)],
                ],
                kwargs: {},
            }).then(function(data) {
                console.log("==========MAIN DATA=============", data, data.find((res) => res.id === self.appointment_id))
                var main_data = data.find((res) => res.id === self.appointment_id)
                if (main_data) {
                    if (main_data.treatment_note) {
                        $('#treatment_note').val(main_data.treatment_note)
                        $("#treatment_note").attr("disabled", "disabled");
                    }
                    if (main_data.treatment_body_note) {
                        $('#treatment_body_note').val(main_data.treatment_body_note)
                        $("#treatment_body_note").attr("disabled", "disabled");
                    }
                }
            });

            // For Getting Face Order Lines
            self.rpc("/web/dataset/call_kw/face.order.line/search_read", {
                model: 'face.order.line',
                method: 'search_read',
                args: [],
                kwargs: {domain: [
                    ['appointment_id', '=', parseInt(self.appointment_id)],
                ],},
            }).then(function(data){
                console.log("=====face.order.line=======DATA=======",data)

                for (var i = 0; i < data.length; i++) {
                    var newRow = $("<tr>")
                    var cols = ""
                    var productSelect = '<select disabled="disabled" class="form-control productFaceRow">'
                    productSelect += '<option value="">Select Material</option>'
                    if(self.products){
                        for (var k = 0; k < self.products.length; k++){
                            if(self.products[k].id == data[i].product_id[0]){
                                productSelect = productSelect + '<option selected="selected" value="' + self.products[k].id + '">' + self.products[k].name + '</option>'
                            }
                            else{
                                productSelect = productSelect + '<option value="' + self.products[k].id + '">' + self.products[k].name + '</option>'
                            }
                        }
                    }
                    productSelect += "</select>"
                    cols += '<td>' + productSelect +'</td>';
                    cols += '<td><input readonly="readonly" type="number" class="form-control inputQauntity" name="quantity" value="'+ data[i].quantity +'"/></td>';
                    cols += '<td><input readonly="readonly" type="number" class="form-control inputUnitPrice" name="unit_price" value="'+ data[i].unit_price +'"/></td>';
                    cols += '<td><input readonly="readonly" type="number" class="form-control" name="subtotal" readonly="readonly" value="'+ data[i].quantity*data[i].unit_price +'"/></td>';
                    cols += '<td><i class="fa fa-trash mt-2 delFaceRow d-none" style="color: red;font-size: 16px;cursor: pointer;"></i></td>';
                    newRow.append(cols)
                    $("#faceMaterialTable").find("tbody").empty();
                    $("#faceMaterialTable").append(newRow)
                    console.log("=========addBodyMaterial=============",$("#addBodyMaterial"))
                    $("#addFaceMaterial").addClass("d-none");
                }
                self._calculationSubtotal(self);
            })


        }
    }

    // Main Body Top Button
    onClickBodyBtn(e) {
        var self = this;
        $('.globle_btn').removeClass('btn-primary text-white')
        $('.globle_btn').addClass('btn-secondary')
        $('#bodyBtn').removeClass('btn-secondary')
        $('#bodyBtn').addClass('btn-primary text-white')

        $('.globleImage').addClass('d-none')
        $('#myCanvasBody').removeClass('d-none')
        $('#myCanvasBodyBtns').removeClass('d-none')
        $('#myCanvasBodyContent').removeClass('d-none')

        if (self.appointment_id) {

            // For Getting Body Chart
            self.rpc("/web/dataset/call_kw/medical.body.markers.history/search_read", {
                model: 'medical.body.markers.history',
                method: 'search_read',
                args: [],
                kwargs: {domain: [
                    ['appointment_id', '=', parseInt(this.appointment_id)],
                ],}
            }).then(function(data) {
                for (var k = 0; k < data.length; k++) {
                    var strCoordinate = data[k]['name']
                    var singleArray = strCoordinate.replace(/'/g, '"');
                    var dataCoor = JSON.parse(singleArray)
                    if (dataCoor) {
                        for (var i = 0; i < dataCoor.length; i++) {
                            var sub_data = dataCoor[i]
                            // var ctxBody = self.$el.find("#myCanvasBody")[0].getContext("2d");
                            var ctxBody = $(self.faceBodyRef.el)[0].getContext("2d");
                            ctxBody.beginPath();
                            ctxBody.strokeStyle = 'black';
                            ctxBody.lineWidth = 6;
                            ctxBody.lineJoin = "round";
                            ctxBody.moveTo(sub_data[0], sub_data[1]);
                            ctxBody.lineTo(sub_data[2], sub_data[3]);
                            ctxBody.closePath();
                            ctxBody.stroke();
                        }
                    }
                }
            })

            // For Getting Main Appointment
            self.rpc("/web/dataset/call_kw/medical.appointment/search_read",{
                model: 'medical.appointment',
                method: 'search_read',
                args: [],
                kwargs: {domain: [
                    ['id', '=', parseInt(self.appointment_id)],
                ]}
            }).then(function(data) {
                console.log("==========MAIN DATA=============", data, data[0])
                if (data) {
                    // if (data[0].treatment_note) {
                    //     $('#treatment_note').val(data[0].treatment_note)
                    //     $("#treatment_note").attr("disabled", "disabled");
                    // }
                    if (data[0].treatment_body_note) {
                        $('#treatment_body_note').val(data[0].treatment_body_note)
                        $("#treatment_body_note").attr("disabled", "disabled");
                    }
                }
            });

            // For Getting Body Order Lines
            self.rpc("/web/dataset/call_kw/body.order.line/search_read", {
                model: 'body.order.line',
                method: 'search_read',
                args: [],               
                kwargs: {domain: [
                    ['appointment_id', '=', parseInt(self.appointment_id)],
                ],}
            }).then(function(data){
                console.log("=====face.order.line=======DATA=======",data)

                for (var i = 0; i < data.length; i++) {
                    var newRow = $("<tr>")
                    var cols = ""
                    var productSelect = '<select disabled="disabled" class="form-control productBodyRow">'
                    productSelect += '<option value="">Select Material</option>'
                    if(self.products){
                        for (var k = 0; k < self.products.length; k++){
                            if(self.products[k].id == data[i].product_id[0]){
                                productSelect = productSelect + '<option selected="selected" value="' + self.products[k].id + '">' + self.products[k].name + '</option>'
                            }
                            else{
                                productSelect = productSelect + '<option value="' + self.products[k].id + '">' + self.products[k].name + '</option>'
                            }
                        }
                    }
                    productSelect += "</select>"
                    cols += '<td>' + productSelect +'</td>';
                    cols += '<td><input readonly="readonly" type="number" class="form-control inputQauntityBody" name="quantity" value="'+ data[i].quantity +'"/></td>';
                    cols += '<td><input readonly="readonly" type="number" class="form-control inputUnitPriceBody" name="unit_price" value="'+ data[i].unit_price +'"/></td>';
                    cols += '<td><input readonly="readonly" type="number" class="form-control" name="subtotal" readonly="readonly" value="'+ data[i].quantity*data[i].unit_price +'"/></td>';
                    cols += '<td><i class="fa fa-trash mt-2 delBodyRow d-none" style="color: red;font-size: 16px;cursor: pointer;"></i></td>';
                    newRow.append(cols)
                    $("#bodyMaterialTable").find("tbody").empty();
                    $("#bodyMaterialTable").append(newRow)
                    $("#addBodyMaterial").addClass("d-none");
                }
                self._calculationSubtotalBody(self);
            })
        }
    }

    Draw(x, y, isDown) {
        if (isDown) {
            var single_cordinate = []
            // console.log("new ages====", $(this.faceRef.el))
            this.ctx = $(this.faceRef.el)[0].getContext("2d");
            this.ctx.beginPath();
            this.ctx.strokeStyle = 'black';
            this.ctx.lineWidth = 5;
            this.ctx.lineJoin = "round";
            this.ctx.moveTo(this.lastX, this.lastY);
            this.ctx.lineTo(x, y);
            this.ctx.closePath();
            this.ctx.stroke();
            single_cordinate.push(this.lastX, this.lastY, x, y);
            this.single_mark.push(single_cordinate)
        }
        this.lastX = x;
        this.lastY = y;
    }

    DrawBody(x, y, isDown) {
        if (isDown) {
            var single_cordinate_body = []
            this.ctxBody = $(this.faceBodyRef.el)[0].getContext("2d");
            this.ctxBody.beginPath();
            this.ctxBody.strokeStyle = 'black';
            this.ctxBody.lineWidth = 5;
            this.ctxBody.lineJoin = "round";
            this.ctxBody.moveTo(this.lastXBody, this.lastYBody);
            this.ctxBody.lineTo(x, y);
            this.ctxBody.closePath();
            this.ctxBody.stroke();
            single_cordinate_body.push(this.lastXBody, this.lastYBody, x, y)
            this.single_mark_body.push(single_cordinate_body)
        }
        this.lastXBody = x;
        this.lastYBody = y;
    }

    onClickEditFaceBtn(ev) {
        this.state.is_edit = false;
    }

    // For Face Mouse Event
    onMouseDownMyCanvas(e) {
        console.log("================e=====17 JS===this====",this)
        console.log("================e=====17 JS====self===",e)
        console.log("================e=====17 JS====self===",$(this.faceRef.el).find("#myCanvas"))
        console.log("================e=====17 JS====self===",$(this.faceRef.el).offset())
       if (!this.state.is_edit) {
           e.preventDefault();
           var self = this;
           this.mousePressed = true;
           this.Draw(e.pageX - $(this.faceRef.el).offset().left, e.pageY - $(this.faceRef.el).offset().top, false);
       }
    }

    _onMouseMoveMyCanvas(e) {
        if (!this.state.is_edit) {
            var self = this
            if (this.mousePressed) {
                this.Draw(e.pageX - $(this.faceRef.el).offset().left, e.pageY - $(this.faceRef.el).offset().top, true);
            }
        }
    }

    _onMouseUpMyCanvas(ev) {
        if (!this.state.is_edit) {
            this.mousePressed = false;
            this.multi_mark.push(this.single_mark)

            console.log("========mouseup=======mouseup==", this.multi_mark)
            this.single_mark = []
        }
    }

    _onClickUndoFaceBtn(ev) {
        var self = this;
        if (this.multi_mark) {
            var lastElement = this.multi_mark.pop();
            //console.log("=============lastElement=====lastElement==",lastElement);
            if (lastElement) {
                for (var i = 0; i < lastElement.length; i++) {
                    var sub_data = lastElement[i]
                    if (!this.ctx){
                        this.ctx = $(this.faceRef.el)[0].getContext("2d");
                    }
                    //this.ctx.clearRect(sub_data[0]-6,sub_data[1]-6,10,10);
                    //this.ctx.clearRect(sub_data[2]-6,sub_data[3]-6,10,10);
                    this.ctx.beginPath();
                    this.ctx.strokeStyle = 'white';
                    this.ctx.lineWidth = 6;
                    this.ctx.lineJoin = "round";
                    this.ctx.moveTo(sub_data[0], sub_data[1]);
                    this.ctx.lineTo(sub_data[2], sub_data[3]);
                    this.ctx.closePath();
                    this.ctx.stroke();
                }
            }
        }
    }

    // Face Buttons Funcnality
    _onClickSaveFaceBtn(ev) {
        var self = this;

        // Save Data New Marks
        if (self.appointment_id && this.multi_mark) {
            for (var i = 0; i < this.multi_mark.length; i++) {
                var data = {
                    'name': this.multi_mark[i],
                    'appointment_id': parseInt(self.appointment_id),
                }
                self.rpc("/web/dataset/call_kw/medical.markers.history/create", {
                    model: 'medical.markers.history',
                    method: 'create',
                    args: [data],
                    kwargs: {},
                })
            }
            this.multi_mark = []
            this.is_edit = true
        }

        // Delete Data Old Marks
        if (self.appointment_id && this.delete_ids) {
            var self = this
            self.rpc("/web/dataset/call_kw/medical.markers.history/unlink", {
                model: 'medical.markers.history',
                method: 'unlink',
                args: [this.delete_ids],
                kwargs: {},
            })
            this.delete_ids = []
        }

    }

    _onClickDeleteFaceBtn(ev) {
        var self = this;

        // Existing Marks Delete
        if (this.multi_mark && !this.state.is_edit) {
            for (var k = 0; k < this.multi_mark.length; k++) {
                var lastElement = this.multi_mark[k]
                for (var i = 0; i < lastElement.length; i++) {
                    var sub_data = lastElement[i]
                    //this.ctx.clearRect(sub_data[0]-6,sub_data[1]-6,10,10);
                    //this.ctx.clearRect(sub_data[2]-6,sub_data[3]-6,10,10);
                    this.ctx.beginPath();
                    this.ctx.strokeStyle = 'white';
                    this.ctx.lineWidth = 7;
                    this.ctx.lineJoin = "round";
                    this.ctx.moveTo(sub_data[0], sub_data[1]);
                    this.ctx.lineTo(sub_data[2], sub_data[3]);
                    this.ctx.closePath();
                    this.ctx.stroke();
                }
            }
            this.multi_mark = []
        }

        // Old Marks Delete
        if (self.appointment_id && !this.state.is_edit) {
            self.rpc("/web/dataset/call_kw/medical.markers.history/search_read", {
                model: 'medical.markers.history',
                method: 'search_read',
                args: [],
                domain: [
                    ['appointment_id', '=', parseInt(this.appointment_id)],
                ],
                kwargs: {}
            }).then(function(data) {
                for (var k = 0; k < data.length; k++) {
                    var strCoordinate = data[k]['name']
                    var mark_id = parseInt(data[k]['id'])
                    console.log("============mark_id========", mark_id)
                    self.delete_ids.push(mark_id)
                    var singleArray = strCoordinate.replace(/'/g, '"');
                    var dataCoor = JSON.parse(singleArray)
                    if (dataCoor) {
                        for (var i = 0; i < dataCoor.length; i++) {
                            var sub_data = dataCoor[i]
                            var ctx = $(self.faceRef.el)[0].getContext("2d");
                            ctx.beginPath();
                            ctx.strokeStyle = 'white';
                            ctx.lineWidth = 7;
                            ctx.lineJoin = "round";
                            ctx.moveTo(sub_data[0], sub_data[1]);
                            ctx.lineTo(sub_data[2], sub_data[3]);
                            ctx.closePath();
                            ctx.stroke();
                        }
                    }
                }
            })
        }
    }

    _onClickEditTreatmentBtn(ev) {
        var self = this;
        console.log("============_onClickEditTreatmentBtn=========", treatment_note)
        $("#treatment_note").attr("disabled", false);
    }

    _onClickSaveTreatmentBtn(ev) {
        var self = this;
        var treatment_note = $('#treatment_note').val()
        console.log("============_onClickSaveTreatmentBtn=========", treatment_note)
        console.log("============_onClickSaveTreatmentBtn=========", self.appointment_id)

        if (self.appointment_id && treatment_note) {
            console.log("============RPC CALL=========")
            self.rpc("/web/dataset/call_kw/medical.appointment/write",{
                model: 'medical.appointment',
                method: 'write',
                args: [
                    [self.appointment_id], {
                        treatment_note: treatment_note,
                    }
                ],
                kwargs: {}
            })
            $("#treatment_note").attr("disabled", "disabled");
        }

    }

    // Treatment Body Buttons Funcnality
    _onClickSaveTreatmentBodyBtn(ev) {
        var self = this;
        var treatment_body_note = $('#treatment_body_note').val()

        if (self.appointment_id && treatment_body_note) {
            self.rpc("/web/dataset/call_kw/medical.appointment/write", {
                model: 'medical.appointment',
                method: 'write',
                args: [
                    [this.appointment_id], {
                        treatment_body_note: treatment_body_note,
                    }
                ],
                kwargs: {}
            })
            $("#treatment_body_note").attr("disabled", "disabled");

        }
    }

    _onClickEditTreatmentBodyBtn(ev) {
        var self = this;
        $("#treatment_body_note").attr("disabled", false);
    }

    _onClickDelFaceRowBtn(ev) {
        var self = this
        ev.currentTarget.closest("tr").remove();
        self._calculationSubtotal(ev)
    }

    _onChangeInputQauntity(ev) {
        var self = this
        self._calculationSubtotal(ev)
    }

    _onChangeInputUnitPrice(ev) {
        var self = this
        self._calculationSubtotal(ev)
    }

    _onChangeProductFaceRow(ev) {
        var self = this
        console.log("=========_onChangeProductFaceRow=======", ev)
        var productId = $(ev.currentTarget).val()
        if (productId) {
            console.log("=======productId======", productId)
            self.rpc("/web/dataset/call_kw/medical.appointment/write",{
                model: 'product.product',
                method: 'search_read',
                args: [],
                kwargs: {domain: [
                    ['id', '=', parseInt(productId)],
                ], fields: ['name', 'lst_price']}
            }).then(function(data) {
                console.log("============productPrice===========", data[0].lst_price)
                if (data) {
                    if (data[0].lst_price) {
                        $(ev.currentTarget).closest("tr").find('td input[name="unit_price"]').val(data[0].lst_price)
                        self._calculationSubtotal(ev)
                    }
                }
            });
        }
    }

    _onClickAddFaceMaterialBtn(ev) {
        var self = this
        console.log("============_onClickAddFaceMaterialBtn=======", self.products)
        var newRow = $("<tr>")
        var cols = ""
        var productSelect = '<select class="form-control productFaceRow">'
        productSelect += '<option value="">Select Material</option>'
        if (self.products) {
            for (var k = 0; k < self.products.length; k++) {
                productSelect = productSelect + '<option value="' + self.products[k].id + '">' + self.products[k].name + '</option>'
            }
        }
        productSelect += "</select>"
        cols += '<td>' + productSelect + '</td>';
        cols += '<td><input type="number" class="form-control inputQauntity" name="quantity" value="1"/></td>';
        cols += '<td><input type="number" class="form-control inputUnitPrice" name="unit_price"/></td>';
        cols += '<td><input type="number" class="form-control" name="subtotal" readonly="readonly"/></td>';
        cols += '<td><i class="fa fa-trash mt-2 delFaceRow" style="color: red;font-size: 16px;cursor: pointer;"></i></td>';
        newRow.append(cols);
        var check_box = $(newRow).find('td .delFaceRow');
        const deleteRow = this._onClickDelFaceRowBtn.bind(this);
        check_box.on("click", deleteRow);

        var productFaceRow = $(newRow).find('td .productFaceRow');
        const changeProduct = this._onChangeProductFaceRow.bind(this);
        productFaceRow.on("change", changeProduct);

        var inputQauntity = $(newRow).find('td .inputQauntity');
        const changeQuantity = this._onChangeInputQauntity.bind(this);
        inputQauntity.on("change", changeQuantity);

        var inputUnitPrice = $(newRow).find('td .inputUnitPrice');
        const changePrice = this._onChangeInputUnitPrice.bind(this);
        inputUnitPrice.on("change", changePrice);
        $("#faceMaterialTable").append(newRow)
    }

    _onClickSaveMaterialBtn(ev) {
        var self = this;

        console.log("============_onClickSaveMaterialBtn=====SAVE====")

        self.rpc("/web/dataset/call_kw/medical.appointment/write", {
                model: 'medical.appointment',
                method: 'write',
                args: [[this.appointment_id], {
                    face_order_line_ids: [[5]],
                }],
                kwargs: {}
           }).then(function(data){
                console.log("============RPC CALL====DATA=====",data)
           })

        $('#faceMaterialTable tbody tr').each(function() {
            var product_id = $(this).find('td select.productFaceRow').val()
            var quantity = $(this).find('td input[name="quantity"]').val()
            var unit_price = $(this).find('td input[name="unit_price"]').val()
            console.log("============product_id========", product_id)
            console.log("============quantity========", quantity)
            console.log("============unit_price========", unit_price)
            if (self.appointment_id && product_id) {
                var data = {
                    'product_id': product_id,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'appointment_id': parseInt(self.appointment_id),
                }
                self.rpc("/web/dataset/call_kw/face.order.line/create", {
                    model: 'face.order.line',
                    method: 'create',
                    args: [data],
                    kwargs: {}
                })
            }
        })

        $('#faceMaterialTable tbody tr').each(function(){
            $(this).find('td select.productFaceRow').attr("disabled", true);
            $(this).find('td input[name="quantity"]').prop('readonly', true);
            $(this).find('td input[name="unit_price"]').prop('readonly', true);
            $(this).find('td .delFaceRow').addClass("d-none");
            $("#addFaceMaterial").addClass("d-none");
        })
    }

    _onClickEditMaterialBtn(ev) {
        //           $("#faces_select").select2().enable(true);
        var self = this;
        console.log("============_onClickEditMaterialBtn=====EDIT==123==",$('#faceMaterialTable'))

       $('#faceMaterialTable tbody tr').each(function(){
            $(this).find('td select.productFaceRow').attr("disabled", false);
            $(this).find('td input[name="quantity"]').prop('readonly', false);
            $(this).find('td input[name="unit_price"]').prop('readonly', false);
            $(this).find('td .delFaceRow').removeClass("d-none");
            $("#addFaceMaterial").removeClass("d-none");
       })
    }

    // BOdy mouse events
    _onMouseDownMyCanvasBody(e) {
        if (!this.state.is_edit_body) {
            e.preventDefault();
            var self = this
            this.mousePressedBody = true;
            this.DrawBody(e.pageX - $(this.faceBodyRef.el).offset().left, e.pageY - $(this.faceBodyRef.el).offset().top, false);
        }
    }

    _onMouseMoveMyCanvasBody(e) {
        if (!this.state.is_edit_body) {
            var self = this
            if (this.mousePressedBody) {
                this.DrawBody(e.pageX - $(this.faceBodyRef.el).offset().left, e.pageY - $(this.faceBodyRef.el).offset().top, true);
            }
        }
    }

    _onMouseUpMyCanvasBody(ev) {
        if (!this.state.is_edit_body) {
            this.mousePressedBody = false;
            this.multi_mark_body.push(this.single_mark_body)
            this.single_mark_body = []
        }
    }

    _onMouseLeaveMyCanvasBody(ev) {
        if (!this.state.is_edit_body) {
            this.mousePressedBody = false;
        }
    }

    //Body buttons functionality

    _onClickEditBodyBtn(ev) {
        this.state.is_edit_body = false;
        console.log("=============_onClickEditBodyBtn===CALL======", )
    }

    _onClickDeleteBodyBtn(ev) {
        var self = this;

        // Existing Marks Delete
        if (this.multi_mark_body && !this.state.is_edit_body) {
            for (var k = 0; k < this.multi_mark_body.length; k++) {
                var lastElement = this.multi_mark_body[k]
                for (var i = 0; i < lastElement.length; i++) {
                    var sub_data = lastElement[i]
                    if (!this.ctxBody){
                        this.ctxBody = $(self.faceBodyRef.el)[0].getContext("2d");
                    }

                    this.ctxBody.beginPath();
                    this.ctxBody.strokeStyle = 'white';
                    this.ctxBody.lineWidth = 7;
                    this.ctxBody.lineJoin = "round";
                    this.ctxBody.moveTo(sub_data[0], sub_data[1]);
                    this.ctxBody.lineTo(sub_data[2], sub_data[3]);
                    this.ctxBody.closePath();
                    this.ctxBody.stroke();
                }
            }
            this.multi_mark_body = []
        }

        // Old Marks Delete
        if (self.appointment_id && !this.state.is_edit_body) {
            self.rpc("/web/dataset/call_kw/face.order.line/create", {
                model: 'medical.body.markers.history',
                method: 'search_read',
                args: [],
                kwargs: {domain: [
                    ['appointment_id', '=', parseInt(this.appointment_id)],
                ],}
            }).then(function(data) {
                for (var k = 0; k < data.length; k++) {
                    var strCoordinate = data[k]['name']
                    var mark_id = parseInt(data[k]['id'])
                    console.log("============mark_id====BODY====", mark_id)
                    self.delete_body_ids.push(mark_id)
                    var singleArray = strCoordinate.replace(/'/g, '"');
                    var dataCoor = JSON.parse(singleArray)
                    if (dataCoor) {
                        for (var i = 0; i < dataCoor.length; i++) {
                            var sub_data = dataCoor[i]
                            var ctxBody = $(self.faceBodyRef.el)[0].getContext("2d");
                            ctxBody.beginPath();
                            ctxBody.strokeStyle = 'white';
                            ctxBody.lineWidth = 7;
                            ctxBody.lineJoin = "round";
                            ctxBody.moveTo(sub_data[0], sub_data[1]);
                            ctxBody.lineTo(sub_data[2], sub_data[3]);
                            ctxBody.closePath();
                            ctxBody.stroke();
                        }
                    }
                }
            })
        }

    }

    _onClickSaveBodyBtn(ev) {
        var self = this;

        // Save Data New Marks
        if (self.appointment_id && this.multi_mark_body) {
            for (var i = 0; i < this.multi_mark_body.length; i++) {
                var data = {
                    'name': this.multi_mark_body[i],
                    'appointment_id': parseInt(self.appointment_id),
                }

                self.rpc("/web/dataset/call_kw/medical.body.markers.history/create", {
                    model: 'medical.body.markers.history',
                    method: 'create',
                    args: [data],
                    kwargs: {}
                })

            }
            this.multi_mark_body = []
            this.state.is_edit_body = true
        }

        // Delete Data Old Marks
        if (self.appointment_id && this.delete_body_ids) {
            var self = this
            self.rpc("/web/dataset/call_kw/medical.body.markers.history/unlink", {
                model: 'medical.body.markers.history',
                method: 'unlink',
                args: [this.delete_body_ids],
                kwargs: {}
            })
            this.delete_body_ids = []
        }

    }

    _onClickUndoBodyBtn(ev) {
        var self = this;
        if (this.multi_mark_body) {
            var lastElement = this.multi_mark_body.pop();
            console.log("=============lastElement=======", lastElement);
            if (lastElement) {
                for (var i = 0; i < lastElement.length; i++) {
                    console.log("====SUB===1=", lastElement[i].length);

                    console.log("====SUB===2=", lastElement[i]);
                    var sub_data = lastElement[i]
                    if (!this.ctxBody){
                        this.ctxBody = $(this.faceBodyRef.el)[0].getContext("2d");
                    }

                    this.ctxBody.beginPath();
                    this.ctxBody.strokeStyle = 'white';
                    this.ctxBody.lineWidth = 6;
                    this.ctxBody.lineJoin = "round";
                    this.ctxBody.moveTo(sub_data[0], sub_data[1]);
                    this.ctxBody.lineTo(sub_data[2], sub_data[3]);
                    this.ctxBody.closePath();
                    this.ctxBody.stroke();

                }
            }
        }
    }

    // Treatment Body Buttons Funcnality
    _onClickSaveTreatmentBodyBtn(ev) {
        var self = this;
        var treatment_body_note = $('#treatment_body_note').val()

        if (self.appointment_id && treatment_body_note) {
            self.rpc("/web/dataset/call_kw/medical.appointment/write", {
                model: 'medical.appointment',
                method: 'write',
                args: [
                    [this.appointment_id], {
                        treatment_body_note: treatment_body_note,
                    }
                ],
                kwargs: {}
            })
            $("#treatment_body_note").attr("disabled", "disabled");

        }
    }

    _onClickEditTreatmentBodyBtn(ev) {
        var self = this;
        $("#treatment_body_note").attr("disabled", false);
    }

    // Body Table Oerations
    _onClickAddBodyMaterialBtn(ev) {
        var self = this
        console.log("============_onClickAddBodyMaterialBtn=======", self.products)
        var newRow = $("<tr>")
        var cols = ""
        var productSelect = '<select class="form-control productBodyRow">'
        productSelect += '<option value="">Select Material</option>'
        if (self.products) {
            for (var k = 0; k < self.products.length; k++) {
                productSelect = productSelect + '<option value="' + self.products[k].id + '">' + self.products[k].name + '</option>'
            }
        }
        productSelect += "</select>"
        
        cols += '<td>' + productSelect + '</td>';
        cols += '<td><input type="number" class="form-control inputQauntityBody" name="quantity" value="1"/></td>';
        cols += '<td><input type="number" class="form-control inputUnitPriceBody" name="unit_price"/></td>';
        cols += '<td><input type="number" class="form-control" name="subtotal" readonly="readonly"/></td>';
        cols += '<td><i class="fa fa-trash mt-2 delBodyRow" style="color: red;font-size: 16px;cursor: pointer;"></i></td>';
        newRow.append(cols);
        // console.log("=========product======", $(newRow).find('td .productBodyRow'))
        var check_box = $(newRow).find('td .delBodyRow');
        const deleteRow = this._onClickDelBodyRowBtn.bind(this);
        check_box.on("click", deleteRow);

        var productBodyRow = $(newRow).find('td .productBodyRow');
        const changeProduct = this._onChangeProductBodyRow.bind(this);
        productBodyRow.on("change", changeProduct);

        var inputQauntityBody = $(newRow).find('td .inputQauntityBody');
        const changeQuantity = this._onChangeInputQauntityBody.bind(this);
        inputQauntityBody.on("change", changeQuantity);

        var inputUnitPriceBody = $(newRow).find('td .inputUnitPriceBody');
        const changePrice = this._onChangeInputUnitPriceBody.bind(this);
        inputUnitPriceBody.on("change", changePrice);

        $("#bodyMaterialTable").append(newRow)
    }

    _onClickDelBodyRowBtn(ev) {
        var self = this
        ev.currentTarget.closest("tr").remove();
        self._calculationSubtotalBody(ev)
    }

    _onChangeInputQauntityBody(ev) {
        var self = this
        self._calculationSubtotalBody(ev)
    }

    _onChangeInputUnitPriceBody(ev) {
        var self = this
        self._calculationSubtotalBody(ev)
    }

    _onChangeProductBodyRow(ev) {
        var self = this
        console.log("=========_onChangeProductFaceRow=======", ev)
        var productId = $(ev.currentTarget).val()
        if (productId) {
            console.log("=======productId======", productId)
            self.rpc("/web/dataset/call_kw/product.product/search_read",{
                model: 'product.product',
                method: 'search_read',
                args: [],
                kwargs: {domain: [
                    ['id', '=', parseInt(productId)],
                ], fields: ['name', 'lst_price']}
            }).then(function(data) {
                console.log("============productPrice===========", data[0].lst_price)
                if (data) {
                    if (data[0].lst_price) {
                        $(ev.currentTarget).closest("tr").find('td input[name="unit_price"]').val(data[0].lst_price)
                        self._calculationSubtotalBody(ev)
                    }
                }
            });
        }
    }

    _onClickSaveMaterialBodyBtn(ev) {
        var self = this;

        console.log("============_onClickSaveMaterialBtn=====SAVE====")

        self.rpc("/web/dataset/call_kw/medical.appointment/write", {
                model: 'medical.appointment',
                method: 'write',
                args: [[this.appointment_id], {
                    body_order_line_ids: [[5]],
                }],
                kwargs: {}
           }).then(function(data){
                console.log("============RPC CALL====DATA=====",data)
           })

        $('#bodyMaterialTable tbody tr').each(function() {
            var product_id = $(this).find('td select.productBodyRow').val()
            var quantity = $(this).find('td input[name="quantity"]').val()
            var unit_price = $(this).find('td input[name="unit_price"]').val()
            if (self.appointment_id && product_id) {
                var data = {
                    'product_id': product_id,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'appointment_id': parseInt(self.appointment_id),
                }
                self.rpc("/web/dataset/call_kw/body.order.line/create",{
                    model: 'body.order.line',
                    method: 'create',
                    args: [data],
                    kwargs: {}
                })
            }
        })

        $('#bodyMaterialTable tbody tr').each(function(){
            $(this).find('td select.productBodyRow').attr("disabled", true);
            $(this).find('td input[name="quantity"]').prop('readonly', true);
            $(this).find('td input[name="unit_price"]').prop('readonly', true);
            $(this).find('td .delBodyRow').addClass("d-none");
            $("#addBodyMaterial").addClass("d-none");
        })

    }

    _onClickEditMaterialBodyBtn(ev) {
       var self = this;
       $('#bodyMaterialTable tbody tr').each(function(){
            $(this).find('td select.productBodyRow').attr("disabled", false);
            $(this).find('td input[name="quantity"]').prop('readonly', false);
            $(this).find('td input[name="unit_price"]').prop('readonly', false);
            $(this).find('td .delBodyRow').removeClass("d-none");
            $("#addBodyMaterial").removeClass("d-none");
       })
    }


}

FaceBodyChart.template = "FaceBodyChartView";

registry.category("actions").add("face_body_chart", FaceBodyChart);