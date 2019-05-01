function toggle_rows( source,
    { selectionName='delete-table-items',
        selectionType='checkbox',
        buttonName='delete-table-items-button',
        buttonType='submit'}) {

    var checkboxes = $(["input[type='", selectionType, "'][name='", selectionName, "']"].join('')),
        button = $(["button[type='", buttonType, "'][name='", buttonName, "']"].join(''));

    for(var i in checkboxes)
        checkboxes[i].checked = source.checked;

    button.attr("disabled", !source.checked);
};

function toggle_row({
    selectionName='delete-table-items',
    selectionType='checkbox',
    buttonName='delete-table-items-button',
    buttonType='submit', }) {

    var checkboxes = $(["input[type='", selectionType, "'][name='", selectionName, "']"].join('')),
        button = $(["button[type='", buttonType, "'][name='", buttonName, "']"].join(''));

    button.attr("disabled", !checkboxes.is(":checked"));
};
