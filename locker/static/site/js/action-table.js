function select_rows(source=undefined, options={}) {
    /* source = undefined - no header selector
     *
     * options = {} - default options:
     *      options.selectionName = 'action-table-column-item' - row selectors names
     *      options.selectionType = 'checkbox' - row selector type
     *      options.buttonName = 'action-table-button' - action button name
     *      options.buttonType = 'submit' - action button type
     *
     * options.selectionName  or selectionType = undefined - no rows checkboxes
     * options.buttonName or buttonType = undefined - no button to toggle */

    if (arguments.length != 2) {return}

    // Default variables
    var selectionName = 'selectionName' in options ? options.selectionName: 'action-table-column-item',
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

$(document).ready(function() {
    // Make table DataTable
    var table = $('.table-container table')

    var datatable_options = {
        "filter": false,
        "retrieve": true,
        "columnDefs": [
            { orderable: false, targets: -1 }
        ]
    }

    // Russian language support
    if ($("select[name='language']").val() == 'ru'){
        datatable_options["language"] = {
            "processing": "Подождите...",
            "search": "Поиск:",
            "lengthMenu": "Показать _MENU_ записей",
            "info": "Записи с _START_ до _END_ из _TOTAL_ записей",
            "infoEmpty": "Записи с 0 до 0 из 0 записей",
            "infoFiltered": "(отфильтровано из _MAX_ записей)",
            "infoPostFix": "",
            "loadingRecords": "Загрузка записей...",
            "zeroRecords": "Записи отсутствуют.",
            "emptyTable": "В таблице отсутствуют данные",
            "paginate": {
                "first": "Первая",
                "previous": "Предыдущая",
                "next": "Следующая",
                "last": "Последняя"
            },
            "aria": {
                "sortAscending": ": активировать для сортировки столбца по возрастанию",
                "sortDescending": ": активировать для сортировки столбца по убыванию"
            }
        }
    }

    // Remove hypelinks from table header
    table.find('th.orderable a').contents().unwrap()

    // Set DataTable paginator buttons classes
    $.fn.dataTable.ext.classes.sPageButton = 'button';
    $.fn.dataTable.ext.classes.sPageButtonActive = 'button-primary';

    // Make DataTable
    table.DataTable(datatable_options);
    table.addClass("hover")
});
