$(document).ready(function () {
    function widgetColumnResize() {
        if ($(window).width() >= 975) {
            // alert($(window).width());
            $('.widget.third-column-lg').each(function () {
                var widget_row = $(this).closest('.row');
                widget_row.detach();
                $('#third_widget_column').append(widget_row);
            });
            $('.widget.second-column-lg').each(function () {
                var widget_row = $(this).closest('.row');
                widget_row.detach();
                tech_widget_column.append(widget_row);
            });
        }
        else {
            $('.widget.third-column-lg').each(function () {
                var widget_row = $(this).closest('.row');
                widget_row.detach();
                tech_widget_column.append(widget_row);
            });
            $('.widget.second-column-lg').each(function () {
                var widget_row = $(this).closest('.row');
                widget_row.detach();
                blog_widget_column.append(widget_row);
            });
        }
    }
});

var welcome_wiget_column = $('#welcome_wiget_column');
var blog_widget_column = $('#first_widget_column');
var tech_widget_column = $('#second_widget_column');

function showBlogPostsOnly() {
    welcome_wiget_column.fadeOut('slow');
    tech_widget_column.fadeOut('slow', function () {
        blog_widget_column.removeClass('col-md-5 col-lg-4');
        blog_widget_column.addClass('offset-lg-2 col-lg-8');
        blog_widget_column.fadeIn('slow');
    });
}

function showTechPostsOnly() {
    welcome_wiget_column.fadeOut('slow');
    blog_widget_column.fadeOut('slow', function () {
        tech_widget_column.addClass('offset-lg-2 col-lg-8');
        tech_widget_column.removeClass('col-md-5 col-lg-4');
        tech_widget_column.fadeIn('slow');
    });
}

function showAllPosts() {
    welcome_wiget_column.fadeOut('slow');
    blog_widget_column.removeClass('offset-lg-2 col-lg-8 col-sm-12');
    tech_widget_column.removeClass('offset-lg-2 col-lg-8 col-sm-12');
    blog_widget_column.addClass('col-md-7 col-lg-8');
    tech_widget_column.addClass('col-md-5 col-lg-4');
    blog_widget_column.fadeIn('slow', function () {
        tech_widget_column.fadeIn('slow');
    });
}
function hideWelcomeWidget() {
    welcome_wiget_column.fadeOut('slow');
}