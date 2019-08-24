$(document).ready(
    function() {
        var current_language = $("select[name='language']").val()
        var created_min = $("#id_created__gte")
        var created_max = $("#id_created__lte")

        // Disable form fields autocomplete
        created_min.attr('autocomplete', 'off');
        created_max.attr('autocomplete', 'off');
        $('#id_id').attr('autocomplete', 'off');
        $('#id_client').attr('autocomplete', 'off');

        // Assign datepicker to filter date fields
        created_min.datepicker($.extend(
                {maxDate: 0, },
                $.datepicker.regional[current_language]
            ));
        created_max.datepicker($.extend(
            {maxDate: 0, },
            $.datepicker.regional[current_language]
        ));

        // Auto submit form when dates changed
        created_min.change(function() {
            $(this).parents("form").submit();
        });
        created_max.change(function() {
            $(this).parents("form").submit();
        });

        // Add autocomplete to filter author field
        var url = "/api/user/autocomplete";
        $.getJSON(url, function(users) {
            $("#id_author").autocomplete({
                source: users,
                select: function(event, ui) {
                    $(this).val(ui.item.value);
                    $(this).parents("form").submit();
                }
            });
        });
    }
);
