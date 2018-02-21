$(document).ready(function () {
    //-- display active nav --//
    var active_nav = $('a[href="' + this.location.pathname + '"]');
    active_nav.parents('li,ul').addClass('active');
    if (active_nav.hasClass('dropdown-item')) {
        active_nav.addClass('active');
    }
    //-- /display active nav --//
});

//-- navbar --//
$('ul.nav a.dropdown-toggle').click(function () {
    if ($(this).parent().hasClass('show')) {
        location.href = $(this).attr('href');
    }
});
//-- /navbar --//