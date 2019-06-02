$(window).on('load', function() {
    $('.loading-progress').remove();
    $('.body-container').css('visibility', 'visible');
});

$(document).ready(function() {
    $("ul.messages").delay(3000). animate(
        {height:"toggle", opacity:"toggle" },
        1000
    );
});
