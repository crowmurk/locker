function add_form(prefix, form, formset) {
    // Add new form in formset
    var form_idx = $(`#id_${prefix}-TOTAL_FORMS`).val();
    $(`#${formset}`).append($(`#${form}`).html().replace(/__prefix__/g, form_idx));
    $(`#id_${prefix}-TOTAL_FORMS`).val(parseInt(form_idx) + 1);
};
