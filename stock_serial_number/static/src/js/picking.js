openerp.stock_serial_number = function(instance){
    instance.stock.PickingEditorWidget.include({

        get_rows: function(){
            // Sobrescribimos todo para añadir use_serial_number a las cols
            var model = this.getParent();
            this.rows = [];
            var self = this;
            var pack_created = [];
            _.each( model.packoplines, function(packopline){
                    var pack = undefined;
                    var color = "";
                    if (packopline.product_id[1] !== undefined){ pack = packopline.package_id[1];}
                    if (packopline.product_qty == packopline.qty_done){ color = "success "; }
                    if (packopline.product_qty < packopline.qty_done){ color = "danger "; }
                    //also check that we don't have a line already existing for that package
                    if (packopline.result_package_id[1] !== undefined && $.inArray(packopline.result_package_id[0], pack_created) === -1){
                        var myPackage = $.grep(model.packages, function(e){ return e.id == packopline.result_package_id[0]; })[0];
                        self.rows.push({
                            cols: { product: packopline.result_package_id[1],
                                    qty: '',
                                    rem: '',
                                    uom: undefined,
                                    lot: undefined,
                                    pack: undefined,
                                    container: packopline.result_package_id[1],
                                    container_id: undefined,
                                    loc: packopline.location_id[1],
                                    dest: packopline.location_dest_id[1],
                                    id: packopline.result_package_id[0],
                                    product_id: undefined,
                                    can_scan: false,
                                    head_container: true,
                                    processed: packopline.processed,
                                    package_id: myPackage.id,
                                    ul_id: myPackage.ul_id[0],
                                    use_serial_number: packopline.use_serial_number  //AÑADIDO
                            },
                            classes: ('success container_head ') + (packopline.processed === "true" ? 'processed hidden ':''),
                        });
                        pack_created.push(packopline.result_package_id[0]);
                    }
                    self.rows.push({
                        cols: { product: packopline.product_id[1] || packopline.package_id[1],
                                qty: packopline.product_qty,
                                rem: packopline.qty_done,
                                uom: packopline.product_uom_id[1],
                                lot: packopline.lot_id[1],
                                pack: pack,
                                container: packopline.result_package_id[1],
                                container_id: packopline.result_package_id[0],
                                loc: packopline.location_id[1],
                                dest: packopline.location_dest_id[1],
                                id: packopline.id,
                                product_id: packopline.product_id[0],
                                can_scan: packopline.result_package_id[1] === undefined ? true : false,
                                head_container: false,
                                processed: packopline.processed,
                                package_id: undefined,
                                ul_id: -1,
                                use_serial_number: packopline.use_serial_number //AÑADIDO
                        },
                        classes: color + (packopline.result_package_id[1] !== undefined ? 'in_container_hidden ' : '') + (packopline.processed === "true" ? 'processed hidden ':''),
                    });
            });
            //sort element by things to do, then things done, then grouped by packages
            group_by_container = _.groupBy(self.rows, function(row){
                return row.cols.container;
            });
            var sorted_row = [];
            if (group_by_container.undefined !== undefined){
                group_by_container.undefined.sort(function(a,b){return (b.classes === '') - (a.classes === '');});
                $.each(group_by_container.undefined, function(key, value){
                    sorted_row.push(value);
                });
            }

            $.each(group_by_container, function(key, value){
                if (key !== 'undefined'){
                    $.each(value, function(k,v){
                        sorted_row.push(v);
                    });
                }
            });

            return sorted_row;
        },
        renderElement: function(){
            var self = this
            this._super();
            this.$('.js_op_table_todo tr').find('td.js_row_qty').each(function(index, elm)
            {   
                var qty_elm = $(elm).find('div form input')
                var minus_elm = $(elm).find('.js_minus')
                var plus_elm = $(elm).find('.js_plus')
                var use_serial = $(qty_elm).attr('data-use_serial_number')
                if ( use_serial == "true" ){
                    qty_elm.prop("readonly", true);
                    plus_elm.hide()
                    minus_elm.hide()
                }
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
                    var selector = '.js_qty[data-op_id=' + packop_id + ']'
                    self.$(selector).val(final_serial_numbers.length)
                    self.$('.js_qty').blur()
                });                
            });
        },

    });
};
