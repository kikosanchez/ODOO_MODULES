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
            $('#o-carousel-product').carousel(image_slider_num);
            return true;
        }

        return false;
    };

    /**
     * CHANGE VARIANT IMAGE ON SELECT
     **/
    $(document).ready(function() {

        $('form.js_add_cart_variants .js_variant_change').on('change', function(){

            var attrIds = [];

            // Loop form inputs to get current values
            $('select.js_variant_change option:selected, input.js_variant_change:checked').each(function() {
                var attr_selected = $(this).val()
                if (attr_selected) attrIds.push(attr_selected);
            });

            // Select combination image if exists
            getAttrCombinations(attrIds).forEach(function(comb) {
                if (slideToImgIfExist(comb)) return;
            });

            // Select single attr image if exists
            slideToImgIfExist($(this).val());

            //$('ol.carousel-indicators li').show();
            //$('ol.carousel-indicators li').not(query_selector).hide();
        }).trigger('change');
    });

})(jQuery);
