(function($) {
    'use strict';
    //var website = odoo.website;
    //website.odoo_website = {};

    console.info('Custom Template Module Running');

    $(document).ready(function() {

        /*
        * MOSTRAR/OCLTAR MENÚ DE CATEGORÍAS
        */

        $('#cat_collapse').click(function(){
            $(this).toggleClass('active');
            $('#products_grid_before > ul.nav').slideToggle();
        });


        /*
         * BOTÓN DE VOLVER ARRIBA
         */

        /*var $goTopBtn = $('#backToTop');

        $(window).scroll(function() {
            if ($(this).scrollTop() >= 460 && $goTopBtn.hasClass('hidden')) $goTopBtn.removeClass('hidden');
            else if ($(this).scrollTop() < 460 && !$goTopBtn.hasClass('hidden')) $goTopBtn.addClass('hidden');
        });

        $goTopBtn.click(function(){
            $('html, body').stop().animate({scrollTop: 0}, 400);
        });*/
    });

})(jQuery);
