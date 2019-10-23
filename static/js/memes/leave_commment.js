// https://hackernoon.com/consume-rest-services-with-ajax-and-csrf-protection-in-django-410ece54690
// https://codeguida.com/post/470
$(document).ready(function () {
    $("form").on("submit", function (event) {
        event.preventDefault();
        var comment = document.getElementById("leave-comment-id").value;
        console.log("comment: " + comment);
        var meme_id = document.getElementById("meme_id").value;
        console.log("meme_id: " + meme_id);
        var author_id = document.getElementById("author_id").value;
        console.log("author_id: " + author_id);
        var data = {"author": author_id, "meme": meme_id, "comment": comment};
        console.log("data: " + data);

        var my_comments_sent = document.getElementById("my_comment_sent");

        $.ajax({
            type: "POST",
            dataType: "json",
            contentType: "application/x-www-form-urlencoded",
            url: "/ajax/comments/",
            data: data,
            "beforeSend": function (xhr, settings) {
                console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            "success": function (result) {
                if (result) {
                    console.log("Post commented!");
                    console.log(result);
                    $('#my_comment').text(result.comment);
                    my_comments_sent.style.display = "block";
                    // TODO: Refresh full comment section to get all newly added comments

                    $.ajax({
                        "type": "GET",
                        "dataType": "json",
                        contentType: "application/json; charset=utf-8",
                        "url": "/ajax/memes/" + meme_id + "/comments/",
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