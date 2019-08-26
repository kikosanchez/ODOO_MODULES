(function() {
    'use strict';

    $(document).ready(function(){

        /**
         * AL SELECCIONAR UNA VARIANTE QUE NO TIENE PRECIO
         * OCULTAMOS LAS OPCIONES DE COMPRA Y MOSTRAMOS EL TEXTO
         * "CONSULTAR PRECIO"
         */

        $('.oe_website_sale').on('change', 'input.js_variant_change, select.js_variant_change, ul[data-attribute_value_ids]', function (ev) {
            var $ul = $(ev.target).closest('.js_add_cart_variants');
            var variant_ids = $ul.data("attribute_value_ids");
            var $parent = $ul.closest('.js_product');
            var $price_wrap = $parent.find(".oe_price:first");

            if(_.isString(variant_ids)) variant_ids = JSON.parse(variant_ids.replace(/'/g, '"'));

            var values = [], unchanged_values = $parent.find('div.oe_unchanged_value_ids').data('unchanged_value_ids') || [];

            $parent.find('input.js_variant_change:checked, select.js_variant_change').each(function () {
                values.push(+$(this).val());
            });

            values =  values.concat(unchanged_values);

            /*
                EJEMPLO VOLCADO variant_ids
                -------------------------------------
                (2) [Array(5), Array(5)]
                0: Array(5)
                    0: 1320 (Variant ID)
                    1: [11175] (Attribute ID)
                    2: 424 (Price)
                    3: 0 (Default Price)
                    4:
                        available_threshold: 5
                        cart_qty: 0
                        custom_message: ""
                        inventory_availability: "always"
                        product_template: 150
                        product_type: "product"
                        uom_name: "Unidad(es)"
                        virtual_available: 25
                    length: 5
                1: (5) [1321, Array(1), 424, 0, {…}]
                length: 2
            */

            for (var k in variant_ids) {
                if (_.isEmpty(_.difference(variant_ids[k][1], values))) {
                    $parent.find("span.no-price").remove();

                    // ID de la variante
                    var current_variant_id = variant_ids[k][0];
                    // Precio de la variante
                    var current_variant_price = variant_ids[k][2];
                    // Se vende si hay stock
                    var current_variant_selled = (variant_ids[k][4].inventory_availability == "always" && variant_ids[k][4].virtual_available > 0)
                    // Se vende si el stock está por encima de un umbral
                    || (variant_ids[k][4].inventory_availability == "threshold" && variant_ids[k][4].virtual_available > variant_ids[k][4].available_threshold)
                    // Se vende independientemente del stock
                    || (variant_ids[k][4].inventory_availability == "never" || variant_ids[k][4].inventory_availability == "custom");

                    if (current_variant_id && current_variant_selled && current_variant_price > 0){
                        // Está disponible y tiene precio
                        $parent.find("#add_to_cart").show();
                        $parent.find("div.css_quantity").show();
                        $price_wrap.show();
                    }else{
                        // No está disponible o no tiene precio
                        var product_name = $('.c_product_name').text();
                        $('<span class="no-price"><hr style="margin-bottom: 12px"/><a href="/contactus" class="btn btn-danger">Consultar precio</a></span>').insertAfter($price_wrap);
                        $parent.find("#add_to_cart").hide();
                        $parent.find("div.css_quantity").hide();
                        $price_wrap.hide();
                    }

                    break;
                }
            }
        }).trigger('change');

    });

})();
