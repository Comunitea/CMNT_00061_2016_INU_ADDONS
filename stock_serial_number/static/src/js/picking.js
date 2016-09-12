openerp.stock_serial_number = function(instance){
    instance.stock.PickingEditorWidget.include({


        renderElement: function(){
            var self = this
            this._super();
            this.$('#js_SerialNumber').on('hide', function () {
                    var id = $(this).data('product-id');
                    var op_id = $(this).parents("[data-id]:first").data('id');
                    self.getParent().scan_product_id(id,true,op_id);
            })
            this.$('.js_assign_serial_number').click(function(event){
                var $ship_modal = self.$el.siblings('#js_SerialNumber');
                $ship_modal.modal();

                $('#js_SerialNumber input[name="use_packop_id"]').val($(event.target).attr('data-id'))

                $('#js_SerialNumber input.js_serial_number').keypress(function(e){
                        if(e.which == 13) {
                        var serial_numbers = $('#js_SerialNumber input.js_serial_number').map(function(idx, elem) {return $(elem).val()});

                        var new_input = $('<input />');
                        new_input.attr('type', 'text');
                        new_input.addClass('form-control text-center js_serial_number');
                        new_input.keypress(arguments.callee); // Asigno evento para keypress en el nuevo input
                        $('#js_SerialNumber table tbody').append($('<tr>').append($('<td>').append(new_input)))
                        new_input.focus()
                    }
                });
                self.$('.js_send_serial_number').click(function(){
                    var $ship_modal = self.$el.siblings('#js_SerialNumber');
                    var serial_numbers = $('#js_SerialNumber input.js_serial_number').map(function(idx, elem) {return $(elem).val()});
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
                    self.$('.js_qty').val(final_serial_numbers.length)
                    self.$('.js_qty').blur()
                });                
            });
        },

    });
};
