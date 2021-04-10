$.fn.select2.defaults.set("theme", "bootstrap4");

$(window).ready(function() {
    // Show page content after loading
    $('.loading-progress').remove();
    $('.container').css('visibility', 'visible');
});

$(document).ready(function() {
    // Hide notification messages
    $(".alert").delay(5000). animate(
        {height:"toggle", opacity:"toggle"},
        1000
    );
});

$(document).ready(function() {
    // Language selector
    $("select[name='language']").select2({
        minimumResultsForSearch: Infinity,
        theme: 'default',
    });

    $('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
        // Dropdown submenus
        if (!$(this).next().hasClass('show')) {
            $(this).parents('.dropdown-menu').first().find('.show').removeClass('show');
        }

        $(this).next('.dropdown-menu').toggleClass('show');

        $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
            $('.dropdown-menu .show').removeClass('show');
        });

        return false;
    });
});

$(document).ready(function () {
    // Highlight curren position in navbar
    var pathname = window.location.pathname;

    $('#navbarMainNavigation a').filter(function() {
        return this.pathname == pathname;
    }).parent().addClass('active');

    $('#navbarMainNavigation a').filter(function() {
        return this.pathname != pathname;
    }).parent().removeClass('active');
});
