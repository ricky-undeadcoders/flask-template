//------ admin all ------//
//-- global variables --//
//-- /global variables --//

//-- actions --//
//-- /actions --//

//--- document.ready ---//
$(document).ready(function () {
    //-- list interaction--//
    $('.row_item').click(function () {
        var row = $(this);
        toggleAllSubData(row);
        row.toggleClass('row_selected');
        row.find('i').toggleClass('fa-chevron-up fa-chevron-down');
        if (row.hasClass('row_selected')) {
            toggleViewSubData('on', row);
        }
        else {
            toggleViewSubData('off_selected', row);
        }
    });
    //-- /list interaction--//

    //-- display active nav --//
    var active_nav = $('a[href="' + this.location.pathname + '"]');
    active_nav.parents('li,ul').addClass('active');
    if (active_nav.hasClass('dropdown-item')) {
        active_nav.addClass('active');
    }
    //-- /display active nav --//
});
//--- /document.ready ---//

function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
//-- /functions --//

//-- navbar --//
$('ul.nav a.dropdown-toggle').click(function () {
    if ($(this).parent().hasClass('show')) {
        location.href = $(this).attr('href');
    }
});
//-- /navbar --//


//-- lists --//
function toggleViewSubData(state, row) {
    var parent_row = $('#sub_data_'.concat(row.attr('id')));
    if (state === 'on') {
        parent_row.fadeIn('fast');
        parent_row.find('.details_parent_div').slideToggle('fast');
        // parent_row.show();
    }
    else if (state === 'off_selected') {
        parent_row.find('.details_parent_div').slideToggle('fast', function () {
            parent_row.hide();
        });
    }
    else if (state === 'off') {
        parent_row.find('.details_parent_div').hide();
        parent_row.hide();
    }
}

function toggleAllSubData(selected_row) {
    $('.row_item').each(function () {
        var row = $(this);
        if (!row.is(selected_row)) {
            if (row.hasClass('row_selected')) {
                row.toggleClass('row_selected');
                row.find('i').toggleClass('fa-chevron-up fa-chevron-down');
                toggleViewSubData('off', row);
            }
        }
    });
}
//-- /lists --//
//------ /admin all ------//