$(document).ready(
    function() {
        // Disable form fields autocomplete
        $('#id_equipment').attr('autocomplete', 'off');
        $('#id_rating__gte').attr('autocomplete', 'off');
        $('#id_rating__lte').attr('autocomplete', 'off');
    }
);
