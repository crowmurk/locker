$(document).ready(function() {
    // Add search option to select fields
    var order_select = $("select[name='order'][id='id_order']");
    var service_select = $("select[name='service'][id='id_service']");

    order_select.select2();
    service_select.select2();
});
