$(document).ready(
    function() {
        // Assign datepicker to filter date fields
        var created_min = $("input[name='created_min']")
        var created_max = $("input[name='created_max']")

        created_min.attr( 'autocomplete', 'off' );
        created_max.attr( 'autocomplete', 'off' );
        created_min.datepicker({dateFormat: 'dd.mm.yy', maxDate: 0 });
        created_max.datepicker({dateFormat: 'dd.mm.yy',  minDate: 0 });
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
