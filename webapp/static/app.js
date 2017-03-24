let send_refresh_request = function(_) {
    $.ajax({
        url: '/refresh',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: display_request_data,
    });
};

let display_request_data = function(data) {
  $('img#sign-image').attr('src', data.current_image_url);
  // Add a date parameter to the url to force refresh of the image.
  let d = new Date();
  $('img#predictions-image').attr('src', data.predictions_url + "?" + d.getTime());
  $('span#tlabel').text(data.truelabel);
}

$(document).ready(function() {
    send_refresh_request({});
    $("button#classify").click(function() {
        send_refresh_request({});
    })

})
