function get_branch_options(branches) {
    // Compose branch selection options
    var options = '<option value="">---------</option>';
    for (var i = 0; i < branches.length; i++) {
        options += [
            `<option value="${branches[i].pk}">`,
                `${branches[i].fields['name']} (${branches[i].fields['address']})`,
            "</option>"
        ].join('');

    }
    return options
}

$(document).ready(function() {
    var current_language = $("select[name='language']").val()
    var client_select = $("#id_client");
    var branch_select = $("#id_branch");

    // Add search option to select fields
    client_select.select2({language: current_language});
    branch_select.select2({language: current_language});

    // Setup chained selection
    if (client_select.val() == '') {
        // In create Order Form
        branch_select.attr('disabled', true);
    }
    else {
        // In edit Order form
        var current_branch_selection = branch_select.val();
        // Get client related branches in JSON
        var url = "/api/client/" + $(client_select).val() + "/branch/json";
        $.getJSON(url, function(branches) {
            // Set branch selection options
            $(branch_select).html(get_branch_options(branches));
            $(branch_select).val(current_branch_selection);
        });
    }
});

$(document).ready(function() {
    $("#id_client").change(function() {
        // Refresh chained selection
        var client_select = $(this);
        var branch_select = $("#id_branch");

        if ($(this).val() == '') {
            // Disable branch selector when no client selected
            $(branch_select).val('');
            $(branch_select).trigger('change')
            $(branch_select).attr('disabled', true);
        }
        else {
            // Get client related branches in JSON
            var url = "/api/client/" + $(this).val() + "/branch/json";
            $.getJSON(url, function(branches) {
                // Set branch selection options
                $(branch_select).html(get_branch_options(branches));
                $(branch_select).attr('disabled', false);
            });
        }
    });
});

$(document).ready(function() {
    // Add search option to formset selects
    // Disable formset fields autocomplete
    var current_language = $("select[name='language']").val()
    var formset = 'options';
    var table = $(`#${formset}_table`);

    // if formset is present
    if (table.length) {
        var selectorsID = `select[id^='id_${formset}-']`;
        var textinputsID = `input[type="text"]input[id^='id_${formset}-']`;
        var selectors = table.find($(selectorsID))
        var textinputs = table.find($(textinputsID))
        var numberOfSelectors = selectors.length;

        // Add search option to selectors
        selectors.select2({language: current_language})
        // Disable autocomplete on text fields
        textinputs.attr('autocomplete', 'off')

        table.bind('DOMSubtreeModified', function() {
            // if new form added in formset
            var newSelectors = table.find($(selectorsID));
            if(newSelectors.length !== numberOfSelectors) {
                numberOfSelectors = newSelectors.length;
                // Add search option to select field in formset
                table.find(
                    $(`select[id^='id_${formset}-${parseInt(numberOfSelectors) - 1}-']`)
                ).select2({language: current_language});
                table.find(
                    $(`input[type="text"]input[id^='id_${formset}-${parseInt(numberOfSelectors) - 1}-']`)
                ).attr('autocomplete', 'off')
            }
        });
    }
});
