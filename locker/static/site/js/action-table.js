function select_rows(source=undefined, options={}) {
    /* source = undefined - no header selector
     *
     * options = {} - default options:
     *      options.selectionName = 'action-column-item' - row selectors names
     *      options.selectionType = 'checkbox' - row selector type
     *      options.buttonName = 'action-table-button' - action button name
     *      options.buttonType = 'submit' - action button type
     *
     * options.selectionName  or selectionType = undefined - no rows checkboxes
     * options.buttonName or buttonType = undefined - no button to toggle */

    if (arguments.length != 2) {return}

    // Default variables
    var selectionName = 'selectionName' in options ? options.selectionName: 'action-column-item',
        selectionType = 'selectionType' in options ? options.selectionType: 'checkbox',
        buttonName = 'buttonName' in options ? options.buttonName: 'action-table-button',
        buttonType = 'buttonType' in options ? options.buttonType: 'submit';

    // Rows checkboxes to toggle if not undefined explicitly
    if (selectionName !== undefined && selectionType !== undefined)
        var checkboxes = $(["input[type='", selectionType, "'][name='", selectionName, "']"].join(''));

    // Delete button to toggle if not undefined explicitly
    if (buttonName !== undefined && buttonType !== undefined)
        var button = $(["button[type='", buttonType, "'][name='", buttonName, "']"].join(''));


    // Toggle row checkboxes
    if (source !== undefined && checkboxes !== undefined)
        for(var i in checkboxes)
            checkboxes[i].checked = source.checked;

    // Toggle delete button
    if (button !== undefined) {
        if (source !== undefined)
            button.attr("disabled", !source.checked);
        if (checkboxes !== undefined)
            button.attr("disabled", !checkboxes.is(":checked"));
    }
};
