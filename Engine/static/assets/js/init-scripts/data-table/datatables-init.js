(function ($) {
    //    "use strict";


    /*  Data Table
    -------------*/

    jQuery('#homeowners_table').DataTable({
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
		responsive:true
    });

})(jQuery);
