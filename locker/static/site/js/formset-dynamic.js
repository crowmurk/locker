$(document).ready(function() {
    $('#formset_add_form_button').click(function() {
        var options = $(this).data();

        // Add new form in formset
        if (options !== undefined) {
            var form_idx = $(`#id_${options.prefix}-TOTAL_FORMS`).val();
            $(`#${options.formset}`).append($(`#${options.form}`).html().replace(/__prefix__/g, form_idx));
            $(`#id_${options.prefix}-TOTAL_FORMS`).val(parseInt(form_idx) + 1);
        }
    });
});
