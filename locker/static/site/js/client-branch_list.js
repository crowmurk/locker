$(document).ready(
    function() {
        // Disable form fields autocomplete
        $('#id_branch').attr('autocomplete', 'off');
        $('#id_client').attr('autocomplete', 'off');
        $('#id_number_of_orders__gte').attr('autocomplete', 'off');
        $('#id_number_of_orders__lte').attr('autocomplete', 'off');
    }
);
