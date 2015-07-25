/**
 * Created by dheerendra on 21/7/15.
 */
var body = $('body');
var fetch_news_url;
var add_news_url;
var $news_form = $("#news-form");

$news_form.bind('reset', function (e) {
   $("#news-image-list").html("");
});

$news_form.submit(function (e) {
    e.preventDefault();
    var submit_url = add_news_url;
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
            $("#news-form")[0].reset();
            $("#news-error-list").empty();
            fetch_news();
            display_notification('success', 'News updated successfully');
        },
        error: function (jqXHR, textStatus, errorThrown) {
            var status = jqXHR.status;
            if (status == 413){
                display_notification('danger', 'Request size two large. Please resize your image to 4 MB');
                return;
            }
            if (status.toString().charAt(0) == "5"){
                display_notification('danger', 'Internal server error. Please try again later');
                return;
            }
            var error_data = JSON.parse(jqXHR.responseText);
            var error_list_selector = $("#news-error-list");
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
                    var element_form_group = $("#news-form input[name={0}]".format(key)).closest('.form-group');
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

function fetch_news() {
    $.ajax({
        url: fetch_news_url,
        success: function (data) {
            $("#news-list").html(data);
        }
    });
}

$(function () {
    fetch_news();
});

function news_nav_control(news) {
    news.preventDefault();
    var href = $(news.target).attr('href');
    if (href != "") {
        fetch_news_url = href;
        fetch_news();
    }
}

body.on('click', '#news-next', function (e) {
    news_nav_control(e);
    return false;
});

body.on('click', '#news-previous', function (e) {
    news_nav_control(e);
    return false;
});

body.on('click', '.news-list-btn', function (e) {
    e.preventDefault();
    var elem = e.target;
    elem = $(elem);
    var id = elem.data('id');
    var description = elem.data('description');
    var category = elem.data('category');
    var designation = elem.data('designation');
    var title = elem.data('title');
    var image = elem.data('news-image');
    var news_image_list = $("#news-image-list");

    $("#news-id").val(id);
    $("#news-title").val(title);
    $("#news-description").val(description);
    $("#news-category").val(category);
    $("#news-designation").val(designation);

    news_image_list.html("");
    var image_array = image.split(",");
    for (var index in image_array){
        news_image_list.append("<a href=\"{0}\" target=_blank>{0}</a>".format(image_array[index]));
    }

});

