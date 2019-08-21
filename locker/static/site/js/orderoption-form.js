$(document).ready(function() {
    // Add search option to select fields
    $("select[name='order'][id='id_order']").select2({language: current_language});
    $("select[name='service'][id='id_service']").select2({language: current_language});
});
