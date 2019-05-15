function get_branch_options(branches) {
    // Compose branch selection options
    var options = '<option value="">---------</option>';
    for (var i = 0; i < branches.length; i++) {
        options += [
            '<option value="', branches[i].pk, '">',
            branches[i].fields['name'],
            ' (', branches[i].fields['address'], ')',
            '</option>'
        ].join('');
    }
    return options
}

$(document).ready(function() {
    var client_select = $("select[name='client'][id='id_client']");
    var branch_select = $("select[name='branch'][id='id_branch']");
    var order_options = $("select[name^='order_options-'][name!='order_options-__prefix__-service']");

    // Add search option to select fields
    client_select.select2();
    branch_select.select2();
    order_options.select2();

    // Setup chained selection
    if (client_select.val() == '') {
        // In create Order Form
        branch_select.attr('disabled', true);
    }
    else {
        // In edit Order form
        var current_branch_selection = branch_select.val();
        // Get client related branches in JSON
        var url = "/client/" + $(client_select).val() + "/jsonbranch";
        $.getJSON(url, function(branches) {
            // Set branch selection options
            $(branch_select).html(get_branch_options(branches));
            $(branch_select).val(current_branch_selection);
        });
    }
});

$(document).ready(function() {
    $("select[name='client'][id='id_client']").change(function() {
        // Refresh chained selection
        var client_select = $(this);
        var branch_select = $("select[name='branch'][id='id_branch']");

        if ($(this).val() == '') {
            // Disable branch selector when no client selected
            $(branch_select).val('');
            $(branch_select).attr('disabled', true);
        }
        else {
            // Get client related branches in JSON
            var url = "/client/" + $(this).val() + "/jsonbranch";
            $.getJSON(url, function(branches) {
                // Set branch selection options
                $(branch_select).html(get_branch_options(branches));
                $(branch_select).attr('disabled', false);
            });
        }
    });
});

$(document).ready(function() {
    // Add search option to select field
    // when new form added in formset
    var order_options_table = $('#order_options_table')

    // if formset is present
    if (order_options_table.length) {
        var order_options_selector = "select[name^='order_options-'][name!='order_options-__prefix__-service']"
        var numberOfForms = $(order_options_selector).length

        order_options_table.bind('DOMSubtreeModified', function() {
            // if new form added in formset
            var order_options = $(order_options_selector)
            if(order_options.length !== numberOfForms){
                numberOfForms = order_options.length;
                // Add search option to select field in formset
                $('#id_order_options-' + (parseInt(numberOfForms) - 1) + '-service').select2();
            }
        });
    }
});
