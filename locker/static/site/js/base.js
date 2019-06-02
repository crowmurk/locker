$(window).on('load', function() {
    $('.loading-progress').remove();
    $('.body-container').css('visibility', 'visible');
});

$(document).ready(function() {
    $("ul.messages").delay(3000).fadeOut(1000, function() {
        $(this).remove();
    });
});
