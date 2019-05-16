$(document).ready(
    function() {
        // Assign datepicker to filter date fields
        var created_min = $("input[name='created_min']")
        var created_max = $("input[name='created_max']")
        var current_language = $("select[name='language']").val()

        created_min.attr('autocomplete', 'off');
        created_max.attr('autocomplete', 'off');

        created_min.datepicker($.extend({maxDate: 0, }, $.datepicker.regional[current_language]));
        created_max.datepicker($.extend({maxDate: 0, }, $.datepicker.regional[current_language]));
    });

$(document).ready(
    function() {
        // Auto submit form when dates changed
        $("input[name='created_min']").change(function() {
            $(this).parents("form").submit();
        });
        $("input[name='created_max']").change(function() {
            $(this).parents("form").submit();
        });
    });
