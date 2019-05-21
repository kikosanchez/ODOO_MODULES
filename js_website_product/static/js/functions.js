(function() {
    'use strict';
    //var website = odoo.website;
    //website.odoo_website = {};

    console.info('Product View Module Running');

    $(document).ready(function(){

        /**
         * ########## PARCHE ##########
         * A VECES NO SE MUESTRA EL STOCK DISPONIBLE, COMO SE CARGA POR AJAX
         * CADA SEGUNDO BUSCAMOS SI EXISTEN MENSAJES DE STOCK Y LOS MOSTRAMOS
         * UNA VEZ QUE SE MUESTRAN SE CANCELA EL INTERVALO
         */

        var itemStockInterval = setInterval(function(){
            $("div.availability_messages2 > div").fadeIn('fast', function(){
                clearInterval(itemStockInterval);
            });
        }, 1000);
        
    });

})();
