$(document).ready(function() {
    var current_language = $("select[name='language']").val()

    // Add search option to select fields
    $("#id_order").select2({language: current_language, width: '100%'});
    $("#id_service").select2({language: current_language, width: '100%'});
});
