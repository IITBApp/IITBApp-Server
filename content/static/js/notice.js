/**
 * Created by dheerendra on 16/7/15.
 */

var body = $('body');
var fetch_notice_url;
var add_notice_url;
var $notice_form = $("#notice-form");

$("#notice-expiration-date").datetimepicker({
    locale: 'en',
    sideBySide: true,
    showClear: true,
    showClose: true,
    format: 'DD-MM-YYYY HH:mm',
    useCurrent: false
});

$notice_form.bind('reset', function(e){
    $("#notice-id").val("-1");
    $(".element-error").remove();
    $("#notice-notify-users-group").addClass("hide");
});

$notice_form.submit(function(e){
    e.preventDefault();
    var submit_url = add_notice_url;
    var data = $(this).serialize();
    $.ajax({
        url: submit_url,
        data: data,
        dataType: 'json',
        type: 'POST',
        success: function(data, textStatus, jqXHR){
            $("#notice-form")[0].reset();
            $("#notice-error-list").empty();
            fetch_notices();
            display_notification('success', 'Notice updated successfully');
        },
        error: function(jqXHR, textStatus, errorThrown){
            var status = jqXHR.status;
            if (status.toString().charAt(0) == "5"){
                display_notification('danger', 'Internal server error. Please try again later');
                return;
            }
            var error_data = JSON.parse(jqXHR.responseText);
            var error_list_selector = $("#notice-error-list");
            error_list_selector.empty();
            for (var key in error_data){
                if (!error_data.hasOwnProperty(key)){
                    continue;
                }
                var error_list = error_data[key];
                for (var index in error_list){
                    var error = error_list[index];
                    error_list_selector.append("<li><b style=\"color:red;\">{0}:</b> {1}</li>".format(error.code, error.message));
                }
            }

        }
    });

});

function fetch_notices(){
    $.ajax({
        url: fetch_notice_url,
        success: function(data){
            $("#notice-list").html(data);
        }
    });
}

$(function(){
    fetch_notices();
});

function notice_nav_control(event){
    event.preventDefault();
    var href = $(event.target).attr('href');
    if (href != ""){
        fetch_notice_url = href;
        fetch_notices();
    }
}

body.on('click', '#notice-next', function(e){
    notice_nav_control(e);
    return false;
});

body.on('click', '#notice-previous', function(e){
    notice_nav_control(e);
    return false;
});

body.on('click', '.notice-list-btn', function(e){
    e.preventDefault();
    var elem = e.target;
    elem = $(elem);
    var id = elem.data('id');
    var description = elem.data('description');
    var priority = elem.data('priority');
    var expiration_date = elem.data('expiration-date');
    var designation = elem.data('designation');
    var title = elem.data('title');

    var date = new Date(expiration_date);
    var formatted_date = date.iitbAppFormat();

    $("#notice-id").val(id);
    $("#notice-title").val(title);
    $("#notice-description").val(description);
    $("#notice-priority").val(priority);
    $("#notice-expiry").val(formatted_date);
    $("#notice-designation").val(designation);

    $("#notice-notify-users-group").removeClass("hide");
    $("#notice-notify-users").prop("checked", false);

});

