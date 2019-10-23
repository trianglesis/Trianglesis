// https://hackernoon.com/consume-rest-services-with-ajax-and-csrf-protection-in-django-410ece54690
// https://codeguida.com/post/470
$(document).ready(function () {
    $("form").on("submit", function (event) {
        event.preventDefault();

        var cooment = document.getElementById("leave-comment-id").value;
        console.log("cooment: " + x);

        var data = $(this).serialize();
        console.log("data: " + data);

        function getFormData($form) {
            var unindexed_array = $form.serializeArray();
            var indexed_array = {};
            $.map(unindexed_array, function (n, i) {
                indexed_array[n['name']] = n['value'];
            });
            return indexed_array;
        }

        var a_data = getFormData($(this));

        console.log("Alt parse " + a_data);
        console.log("Alt parse meme " + a_data.meme);
        console.log("Alt parse author " + a_data.author);

        $.ajax({
            "type": "POST",
            contentType: "application/x-www-form-urlencoded",
            "url": "/ajax/comments/",
            "data": data,
            "beforeSend": function (xhr, settings) {
                console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            "success": function (result) {
                if (result) {
                    console.log("Post commented!");
                    console.log(result);
                    $('#my_comment').text(result.comment);
                    // TODO: Refresh full comment section to get all newly added comments

                    $.ajax({
                        "type": "GET",
                        "dataType": "json",
                        contentType: "application/json; charset=utf-8",
                        "url": "/ajax/memes/" + a_data.meme + "/comments/",
                        "beforeSend": function (xhr, settings) {
                            console.log("Before Send");
                            $.ajaxSettings.beforeSend(xhr, settings);
                        },
                        "success": function (result) {
                            if (result) {
                                console.log("Post comments refresh!");
                                console.log(result);
                            } else {
                                console.log("No comments for meme!");
                            }
                        },
                    });

                } else {
                    console.log("Post NOT commented!");
                    console.log(result);
                }
            },
        });
        this.reset();
    });
});