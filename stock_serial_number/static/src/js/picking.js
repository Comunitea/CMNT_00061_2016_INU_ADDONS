openerp.stock_serial_number = function(instance){
    instance.stock.PickingEditorWidget.include({


        renderElement: function(){
            var self = this
            this._super();
            this.$('.js_assign_serial_number').click(function(event){
                // debugger;
                var $ship_modal = self.$el.siblings('#js_SerialNumber');
                $ship_modal.modal();
                $('#js_SerialNumber input[name="use_packop_id"]').val($(event.target).attr('data-id'))
                $('#js_SerialNumber input.serial_number').focusout(function(){
                    var serial_numbers = $('#js_SerialNumber input.serial_number').map(function(idx, elem) {return $(elem).val()});
                    var empty_vals = []
                    for (var i = 0; i < serial_numbers.length; i++) {
                        if (serial_numbers[i] === ''){
                            empty_vals.push(serial_numbers[i]);
                        }
                    }
                    // TODO: Intentar que no añada más lineas que la cantidad de por hacer.
                    if(empty_vals.length < 3){
                        var new_input = $('<input />');
                        new_input.attr('type', 'text');
                        new_input.addClass('form-control text-center serial_number');
                        new_input.focusout(arguments.callee);
                        $('#js_SerialNumber table tbody').append($('<tr>').append($('<td>').append(new_input)))
                    }
                    // debugger;
                });
                
            });
            this.$('.js_send_serial_number').click(function(){
                    var $ship_modal = self.$el.siblings('#js_SerialNumber');
                    var serial_numbers = $('#js_SerialNumber input.serial_number').map(function(idx, elem) {return $(elem).val()});
                    var final_serial_numbers = []
                    for (var i = 0; i < serial_numbers.length; i++) {
                        if (serial_numbers[i] !== ''){
                            final_serial_numbers.push(serial_numbers[i]);
                        }
                    }
                    var packop_id = $('#js_SerialNumber input[name="use_packop_id"]').val();
                    new instance.web.Model('stock.pack.operation').call(
                        'set_serial_numbers', [[parseInt(packop_id)], final_serial_numbers]);
                    var $ship_modal = self.$el.siblings('#js_SerialNumber');
                    $ship_modal.modal('hide')
                    // TODO: Llamar a la funcion refresh_ui con el picking_id ???
                });
        },

    });
};
