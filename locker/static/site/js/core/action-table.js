$(document).ready(function() {
    // Make table action-table
    $(".action-table-container").actiontable()
})

$(document).ready(function() {
    // Make table DataTable
    var table = $('.table-container table')

    var datatable_options = {
        "filter": false,
        "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
        "retrieve": true,
        "columnDefs": [
            { targets: 'orderable', orderable: true },
            { targets: '_all', orderable: false }
        ],
        "order": [],
        preDrawCallback: function (settings) {
            var api = new $.fn.dataTable.Api(settings);
            var pagination = $(this)
                .closest('.dataTables_wrapper')
                .find('.dataTables_paginate');
            pagination.toggle(api.page.info().pages > 1);
        }
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
        var length_menu_all_index = datatable_options['lengthMenu'][1].indexOf('All');
        if (length_menu_all_index !== -1) {
            datatable_options['lengthMenu'][1][length_menu_all_index] = 'Все';
        }
    }

    // Make DataTable
    table.addClass("table table-hover")

    // Remove hypelinks from table header
    table.find('th.orderable a').contents().unwrap()

    // Make DataTable
    table.DataTable(datatable_options);
});
