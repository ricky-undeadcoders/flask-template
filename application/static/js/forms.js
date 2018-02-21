//-- global variables --//
var serialized_forms = {};
//-- /global variables --//

//-- actions --//
$(document).ready(function () {
    serialized_forms = {};

    serializeForms();
    updateFormSubmit();
});

$('form :input').on('change input focus', function() {
    updateFormSubmit();
});

$('input[type=file]').change(function () {
    var parent_form = $(this).closest('form');
    var fieldVal = $(this).val();
    if (fieldVal != undefined || fieldVal != "") {
        parent_form.find('#submit').prop('disabled', false);
    }
    else {
        parent_form.find('#submit').prop('disabled', true);
    }
});
//-- /actions --//

//-- functions --//
function serializeForms() {
    $('form').each(function() {
        serialized_forms[$(this).attr('id')] = $(this).serialize();
    });
}

function detectFormChange(form) {
    if (form.serialize() !== serialized_forms[form.attr('id')]) {
        return true;
    }
}

function detectFormErrors(form) {
    if (form.find('.error').not('label, span, ul').length !== 0) {
        return true;
    }
}

function detectEmptyRequiredFields(form) {
    if (form.find('input[aria-required="true"]').not('.valid').length !== 0) {
        return true;
    }
}

function updateFormSubmit() {
    $('form').each(function() {
        var form = $(this);
        var form_id = form.attr('id');
        var form_exceptions = ['about_form', 'quill_form'];
        // custom code for project goes here //
        // /custom code for project goes here //
        if ($.inArray($(this).attr('id'), form_exceptions) === -1) {
            var form_submit = form.find(':submit');
            var unique_primary_submits = {'user_settings_change_password_form': 'change_password_submit'}; //{'new_event_form': 'new'}; // add unique primary submits to this object w/ form id (only characters before '_{{ id }}') selector as key and submit button ID as value

            if ((detectFormChange(form) && !detectFormErrors(form)) && !detectEmptyRequiredFields(form)) {
                form_submit.prop('disabled', false);
            }
            else {
                form_submit.prop('disabled', true);
            }
            $.each(unique_primary_submits, function (key, value) {
                if (typeof form_id !== 'undefined') {
                    if (form_id === key) {
                        var unique_submit = form.find('#' + value);
                        if (unique_submit.length <= 0) {
                            unique_submit = $('#' + value + '[form="' + key + '"]');
                        }
                        if ((detectFormChange(form) && !detectFormErrors(form)) && !detectEmptyRequiredFields(form)) {
                            unique_submit.prop('disabled', false);
                        }
                        else {
                            unique_submit.prop('disabled', true);
                        }
                    }
                }
            });
        }
    });
}


$('.status-btn').click(function () {
    var status_btn = $(this);
    var parent_row = status_btn.parents('.sub_data_parent');
    var status_group = parent_row.find('.status_group');
    var status_icon = status_group.find('.status-icon');
    status_group.toggleClass('row-item-active row-item-inactive');
    status_btn.toggleClass('deactivate-row-item-btn activate-row-item-btn');
    status_icon.find('i').toggleClass('fa-check-circle-o fa-times-circle-o');
    status_btn.find('i').toggleClass('fa-toggle-off fa-toggle-on');
    if (status_btn.hasClass('activate-row-item-btn')){
        status_icon.find('i').attr('title', 'Inactive');
        status_btn.find('i').attr('title', 'Activate');
        parent_row.find('input[name="active_input"]').val('off');
        parent_row.find('input[name="active"]').val('off');
    }
    else if (status_btn.hasClass('deactivate-row-item-btn')) {
        status_icon.find('i').attr('title', 'Active');
        status_btn.find('i').attr('title', 'Deactivate');
        parent_row.find('input[name="active_input"]').val('on');
        parent_row.find('input[name="active"]').val('on');
    }
    updateFormSubmit();
});
//-- /functions --//
