$(document).ready(
    // Disable branch selector
    $("select[name='branch'][id='id_branch']").attr('disabled', true)
)

$(document).ready(
    function() {
        $("select[name='client'][id='id_client']").change(function() {
            var client_select = $(this)
            var branch_select = $("select[name='branch'][id='id_branch']")

            if ($(this).val() == '') {
                // Disable branch selector when no client selected
                $(branch_select).val('');
                $(branch_select).attr('disabled', true);
            }
            else {
                // Get client related branches in JSON
                var url = "/client/" + $(this).val() + "/jsonbranch";
                $.getJSON(url, function(branches) {
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
                    // Set branch selection options
                    $(branch_select).html(options);
                    $(branch_select).attr('disabled', false);
                });
            }
        });
    }
);
