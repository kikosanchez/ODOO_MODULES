odoo.define('js_flipbook', function (require) {    
    "use strict";
    $(document).ready(function(){
        $("ul.nav li a[href$='.pdf']").attr("target", "_blank");
    });
});