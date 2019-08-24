$(document).ready(function() {
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
        "columnDefs": [
            { orderable: false, targets: -1 }
        ]
    }

    // Remove hypelinks from table header
    table.find('th.orderable a').contents().unwrap()

    // Make DataTable
    table.DataTable(datatable_options);
    table.addClass("hover")
    $('.table-container').css("margin-bottom", "30px")
})
