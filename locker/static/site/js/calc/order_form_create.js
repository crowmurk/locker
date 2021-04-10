$(document).ready(function() {
    // Forbid button wrap
    var client = $("#id_client")
    var client_create = $("#id_client_create")

    client.parent().addClass('form-row no-gutters')
    client.wrap('<div class="col"></div>')
    client_create.wrap('<div class="col-auto"></div>')

    // Make table DataTable
    $(".action-table-container").actiontable()

    var table = $('.table-container table')

    var datatable_options = {
        "filter": false,
        "info": false,
        "retrieve": true,
        "scrollY": "50vh",
        "scrollCollapse": true,
        "paging": false,
    }

    // Remove hypelinks from table header
    table.find('th.orderable a').contents().unwrap()

    // Make DataTable
    table.DataTable(datatable_options);
    table.addClass("table-hover")
})
