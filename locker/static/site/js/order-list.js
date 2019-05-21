$(document).ready(
    function() {
        // Assign datepicker to filter date fields
        var created_min = $("input[name='created__gte']")
        var created_max = $("input[name='created__lte']")
        var current_language = $("select[name='language']").val()

        created_min.attr('autocomplete', 'off');
        created_max.attr('autocomplete', 'off');

        created_min.datepicker($.extend({maxDate: 0, }, $.datepicker.regional[current_language]));
        created_max.datepicker($.extend({maxDate: 0, }, $.datepicker.regional[current_language]));
    });

$(document).ready(
    function() {
        // Add autocomplete to filter author field
        var url = "/api/user/autocomplete";
        $.getJSON(url, function(users) {
            $("input[type='text'][name='author']").autocomplete({
                source: users,
                select: function() {$(this).parents("form").submit();}
            });
        });
    });

$(document).ready(
    function() {
        // Auto submit form when dates changed
        $("input[name='created__gte']").change(function() {
            $(this).parents("form").submit();
        });
        $("input[name='created__lte']").change(function() {
            $(this).parents("form").submit();
        });
    });
