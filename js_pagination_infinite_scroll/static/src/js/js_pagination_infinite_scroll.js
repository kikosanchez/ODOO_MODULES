/*
* PAGINACIÓN CON SCROLL
*/

odoo.define('js_pagination_infinite_scroll', function (require) {
    "use strict";

    require('web.dom_ready');
    var Class = require('web.Class');

    var JsPagination = Class.extend({

        init: function () {

            var self = this;
            self.loadingContent = false;
            self.productsTableSelector = '#product-grid-table';
            self.paginationSelector = 'ul.pagination';
            self.productSelector = 'div.oe_product';
            self.loadingIconPosition = '#products_grid';

            // Iniciar la paginación
            $('div.filter-show').remove();
            $(self.paginationSelector).not(':last').remove().end().hide();
            var $productstable = $(self.productsTableSelector), $productsContainer = $productstable.find('tr:last td');

            // Soluciona errores HTTPS Mixed Content
            if (window.location.protocol == 'https:') $('head').append('<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">');

            // Ejecutamos las acciones en este rango de medidas ya que el tema tiene un error y no muestra nada
            if ($(window).width()>900 && $(window).width()<1000) self.loadProductsActions();

            // Cada vez que se hace scroll
            $(window).scroll(function() {

                var $paginationElement = $(self.paginationSelector).last();

                // Si existen los productos y la paginación
                if ($productsContainer.length && $paginationElement.length){

                    var $nextPageLink = $paginationElement.find('li:last-child a');
                    var scrollEnds = ($(window).scrollTop() + $(window).height() > $(document).height() - 500);
                    // Si estamos en el final de la página cargamos la siguiente siempre que el enlace no esté deshabilitado (eso significa que no hay más)
                    if(scrollEnds && !$nextPageLink.parent().hasClass('disabled') && !self.loadingContent) self.loadNextpage($productstable, $productsContainer, $paginationElement, $nextPageLink);

                }

            }); // End Window Event Scroll

            console.log('JsPagination Initialized!');

        },
        loadProductsActions: function () {

            $.getScript(window.location.origin +  '/clarico_shop/static/src/js/clarico_shop.js');
            $.getScript(window.location.origin +  '/clarico_wishlist/static/src/js/wishlist_script.js');
            $.getScript(window.location.origin +  '/website_sale_wishlist/static/src/js/website_sale_wishlist.js');
            $.getScript(window.location.origin +  '/clarico_quick_view/static/src/js/quick_view.js');
            $.getScript(window.location.origin +  '/clarico_similar_product/static/src/js/similar_product.js');
            //console.log('JsPagination Actions Loaded!');

        },
        loadNextpage: function($productstable, $productsContainer, $paginationElement, $nextPageLink){

            var self = this;
            self.loadingContent = true;
            var nextPageUrl = window.location.origin + $nextPageLink.attr('href'), $pagContainer = $paginationElement.parent();
            $(self.loadingIconPosition).append('<div class="page-loading"><img src="/js_pagination_infinite_scroll/static/src/img/timer.gif" width="48" height="54" /></div>');

            console.log('Getting Page', nextPageUrl);

            // Obtenemos la página por Ajax
            $.get(nextPageUrl, function( response ){

                $(self.loadingIconPosition).find('.page-loading').remove();
                var $responseHtml = $('<div />').html(response), $newPagination = $responseHtml.find(self.paginationSelector).last().hide();

                // Recorremos los productos de la nueva página
                $responseHtml.find(self.productSelector).each(function( index ) {
                    // Añadimos una copia a la página actual
                    $productsContainer.append($(this).clone());
                });

                //hideIncompleteRow($productstable, $productsContainer);

                if ($(window).width()>900) self.loadProductsActions();

                // Actualizamos la paginación
                $paginationElement.remove();
                $newPagination.appendTo($pagContainer);
                self.loadingContent = false;

            });
        }
    });

    new JsPagination();
});
