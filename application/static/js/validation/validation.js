//---------------------------------------//
//-------- UCS Validation v1.1.0 --------//
//---------------------------------------//

//-- Configure unique forms by form ID --//
var form_dict = [
    {
        formName: "user_settings_change_password_form",
        requiredFields: ['new_password', 'confirm_password', 'current_password']
    }
];

//-- Configure bulk list forms by form class --//
var bulk_form_dict = [
    {
        formName: "user-form",
        requiredFields: ['username_input', 'first_name_input', 'last_name_input', 'email_input']
    },
    {
        formName: "admin-user-form",
        requiredFields: ['username_input', 'first_name_input', 'last_name_input', 'email_input']
    },
    {
        formName: "role-form",
        requiredFields: ['name_input', 'description_input']
    },
    {
        formName: "admin-role-form",
        requiredFields: ['name_input', 'description_input']
    },
    {
        formName: "blog-post-form",
        requiredFields: ['author', 'title']
    }
];

$(document).ready(function () {
    //-- Validation Functions --//
    function errorPlacementFunction (error, element, unique_class, tooltip_placement) {
        var error_msg = error.text();
        var error_parent = '<div class="validation-icon validation-icon-{0}"></div>'.replace('{0}', unique_class);
        var validation_icon = $('<span class="val-icon-tooltip" type="button" data-toggle="tooltip" data-placement="{0}" title="{1}"><i class="fa fa-exclamation-circle" aria-hidden="true"></i></span>'.replace('{0}', tooltip_placement).replace('{1}', error_msg));
        error.addClass("validation-msg hidden error");
        error.insertBefore(element).wrap(error_parent);
        error.closest('div').prepend(validation_icon);
        validation_icon.tooltip();
    }

    function showErrorsFunction (errorMap, errorList) {
        $.each(errorList, function() {
            if ($(this.element).hasClass('error')) {
                $(this.element).prev('div').find('.val-icon-tooltip').attr('data-original-title', this.message);
                $(this.element).prev('div').find('.val-icon-tooltip').show();
            }
        });
    }

    function successFunction (error) {
        error.prev('.val-icon-tooltip').hide();
    }

    $.each(form_dict, function (i, form) {
        var form_name = form.formName;
        var required_fields = form.requiredFields;
        var rules_dict = {};
        $.each(required_fields, function (index, value) {
            rules_dict[value] = {required:true};
        });

        $('#' + form_name).validate({
            ignore: [],
            rules: rules_dict,
            errorElement: "span",
            errorPlacement: function ( error, element ) {
                errorPlacementFunction(error, element, 'generic', 'right');
            },
            showErrors: function(errorMap, errorList) {
                showErrorsFunction(errorMap, errorList);
                this.defaultShowErrors();
            },
            success: function(error) {
                successFunction(error);
            },
            onfocusout: function ( element ) {
                this.element( element );
            },
            onkeyup: function( element, event ) {
                this.element(element);
            },
            onclick: function ( element, event ) {
                this.element(element);
            }
        });
    });

    $.each(bulk_form_dict, function (i, form) {
        var form_name = form.formName;
        var required_fields = form.requiredFields;
        var rules_dict = {};
        $.each(required_fields, function (index, value) {
            rules_dict[value] = {required:true};
        });

        $('form.' + form_name).each(function() {
            $(this).validate({
                ignore: [],
                rules: rules_dict,
                errorElement: "span",
                errorPlacement: function ( error, element ) {
                    errorPlacementFunction(error, element, 'generic', 'right');
                },
                showErrors: function(errorMap, errorList) {
                    showErrorsFunction(errorMap, errorList);
                    this.defaultShowErrors();
                },
                success: function(error) {
                    successFunction(error);
                },
                onfocusout: function ( element ) {
                    this.element( element );
                },
                onkeyup: function( element, event ) {
                    this.element(element);
                },
                onclick: function ( element, event ) {
                    this.element(element);
                }
            });
        });
    });
});