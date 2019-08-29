(function($) {
    'use strict';

    /**
     * GET ARRAY OF POSIBLE COMBINATIONS FROM IDS ARRAY
     **/
    var getAttrCombinations = function(idsArray){
        let combs = [];

        for (let i = 0; i < idsArray.length - 1; i++) {
            for (let j = i + 1; j < idsArray.length; j++) {
                // Normal conbination
                combs.push(idsArray[i] + ', ' + idsArray[j]);
                // Reversed combination
                combs.push(idsArray[j] + ', ' + idsArray[i]);
            }
        }

        return combs;
    };

    /**
     * CAROUSEL SLIDE TO IMAGE IF IS FOUND
     **/
    var slideToImgIfExist = function(dataVariants){
        var query_selector = 'li[data-variants*="' + dataVariants + '"]';
        var $attr_images = $('ol.carousel-indicators').find(query_selector);
        var image_slider_num = parseInt($attr_images.attr('data-slide-to'));

        if (!isNaN(image_slider_num)){
            console.log('SLIDE TO', image_slider_num);
            console.log('HIDE', query_selector);
            $('#o-carousel-product').carousel(image_slider_num);
            $('ol.carousel-indicators li').css('opacity', 1);
            $('ol.carousel-indicators li').not(query_selector).css('opacity', 0.2);
            return true;
        }

        return false;
    };

    /**
     * CHANGE VARIANT IMAGE ON SELECT
     **/
    $(window).load(function() {

        // Launch at start (one time)
        setTimeout(function(){

            var $formInputs = $('form.js_add_cart_variants .js_variant_change');

            // Launch when a input is changed
            $formInputs.on('change', function(e){
                e.stopPropagation();
                var attrIds = [];

                // Loop form inputs to get current values
                $('select.js_variant_change option:selected, input.js_variant_change:checked').each(function() {
                    var attr_selected = $(this).val()
                    if (attr_selected) attrIds.push(attr_selected);
                });

                // Select combination image if exists
                if (!getAttrCombinations(attrIds).some(slideToImgIfExist) && !slideToImgIfExist($(this).val()))
                    slideToImgIfExist($formInputs.first().val());
            });

            $formInputs.first().trigger('change');

        }, 200);

    });

})(jQuery);
