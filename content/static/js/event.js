/**
 * Created by dheerendra on 21/7/15.
 */
var body = $('body');
var event_fetch_url = '/content/api/event/';
var $event_form = $("#event-form");

$("#event-time-date").datetimepicker({
    locale: 'en',
    sideBySide: true,
    showClear: true,
    showClose: true,
    format: 'DD-MM-YYYY HH:mm',
    useCurrent: false
});

$event_form.bind('reset', function (e) {
   $("#event-image-list").html("");
});

$event_form.submit(function (e) {
    e.preventDefault();
    var submit_url = "/content/add_event/";
    var data = new FormData($(this)[0]);
    $.ajax({
        url: submit_url,
        data: data,
        dataType: 'json',
        type: 'POST',
        cache: false,
        contentType: false,
        processData: false,
        success: function (data, textStatus, jqXHR) {
            $("#event-form")[0].reset();
            $("#event-error-list").empty();
            fetch_events();
            $.notify({
                message: 'Event updated successfully'
            }, {
                type: 'success',
                placement: {
                    from: 'top',
                    align: 'center'
                }
            })
        },
        error: function (jqXHR, textStatus, errorThrown) {
            var error_data = JSON.parse(jqXHR.responseText);
            var error_list_selector = $("#event-error-list");
            error_list_selector.empty();
            $(".element-error").remove();
            for (var key in error_data) {
                if (!error_data.hasOwnProperty(key)) {
                    continue;
                }
                var error_list = error_data[key];
                if (key == '__all__') {
                    for (var index in error_list) {
                        var error = error_list[index];
                        error_list_selector.append("<li><b style=\"color:red;\">{0}:</b> {1}</li>".format(error.code, error.message));
                    }
                }
                else{
                    var element_form_group = $("#event-form input[name={0}]".format(key)).closest('.form-group');
                    var element_error_html = "<ul class=\"element-error\">";
                    for (var index in error_list){
                        var error = error_list[index];
                        element_error_html += "<li><b style=\"color:red;\">{0}:</b> {1}</li>".format(error.code, error.message);
                    }
                    element_error_html += "</ul>";
                    element_form_group.append(element_error_html);
                }
            }
        }
    });

});

function fetch_events() {
    $.ajax({
        url: event_fetch_url,
        success: function (data) {
            $("#event-list").html(data);
        }
    });
}

$(function () {
    fetch_events();
});

function event_nav_control(event) {
    event.preventDefault();
    var href = $(event.target).attr('href');
    if (href != "") {
        event_fetch_url = href;
        fetch_events();
    }
}

body.on('click', '#event-next', function (e) {
    event_nav_control(e);
    return false;
});

body.on('click', '#event-previous', function (e) {
    event_nav_control(e);
    return false;
});

body.on('click', '.event-list-btn', function (e) {
    e.preventDefault();
    var elem = e.target;
    elem = $(elem);
    var id = elem.data('id');
    var description = elem.data('description');
    var category = elem.data('category');
    var event_time = elem.data('event-time');
    var event_place = elem.data('event-place');
    var designation = elem.data('designation');
    var title = elem.data('title');
    var image = elem.data('event-image');
    var event_image_list = $("#event-image-list");

    var date = new Date(event_time);
    var formatted_date = date.iitbAppFormat();

    $("#event-id").val(id);
    $("#event-title").val(title);
    $("#event-description").val(description);
    $("#event-category").val(category);
    $("#event-time").val(formatted_date);
    $("#event-place").val(event_place);
    $("#event-designation").val(designation);

    event_image_list.html("");
    var image_array = image.split(",");
    for (var index in image_array){
        event_image_list.append("<a href=\"{0}\" target=_blank>{0}</a>".format(image_array[index]));
    }

});

