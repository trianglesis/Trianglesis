// https://hackernoon.com/consume-rest-services-with-ajax-and-csrf-protection-in-django-410ece54690
// https://codeguida.com/post/470
$(document).ready(function() {
    $(".like-button").on('click', function(e) {
        e.preventDefault();

        let $this = $(this);
        let MemeId = $this.attr('value');
        console.log("var id = " + MemeId);

        $.ajax({
            "type": "POST",
            "dataType": "json",
            contentType: "application/json; charset=utf-8",
            "url": "/ajax/memes/"+MemeId+"/liking/",
            "beforeSend": function(xhr, settings) {
                console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
                },
            "success": function(result) {
                if (result.likes){
                    console.log("Post Liked!"+MemeId);
                    console.log(result);

                    $('#likes-'+MemeId).text(result.likes);

                    console.log("Got who liked! "+MemeId);
                    var result_likers = result.likers;
                    var actual_likers = "";

                    for (i = 0; i < result_likers.length; i++) {
                        actual_likers += result_likers[i].username+" ";
                    }
                    console.log(actual_likers);
                    $('#who_like-'+MemeId).text(actual_likers);
                } else {
                    console.log("No result for meme "+MemeId);
                    $('#likes-' + MemeId).text(0);
                    $('#who_like-' + MemeId).text("");
                }
            },
        });
        // $.ajax({
        //     "type": "GET",
        //     "dataType": "json",
        //     contentType: "application/json; charset=utf-8",
        //     "url": "/ajax/memes/"+MemeId+"/likes/",
        //     "beforeSend": function(xhr, settings) {
        //         console.log("Before Send");
        //         $.ajaxSettings.beforeSend(xhr, settings);
        //         },
        //     "success": function(result) {
        //         if (result[0]){
        //             console.log("Got who liked! "+MemeId);
        //             console.log(result);
        //             var likers = "";
        //             for (i = 0; i < result.length; i++) {
        //                 likers += result[i].username+" ";
        //             }
        //             console.log(likers);
        //             $('#who_liked-'+MemeId).text(likers);
        //         } else {
        //             console.log("No result for meme "+MemeId);
        //         }
        //     },
        // });
    });

    $(".dislike-button").on('click', function(e) {
        e.preventDefault();

        let $this = $(this);
        let MemeId = $this.attr('value');
        console.log("var id = " + MemeId);

        $.ajax({
            "type": "POST",
            "dataType": "json",
            contentType: "application/json; charset=utf-8",
            "url": "/ajax/memes/"+MemeId+"/disliking/",
            "beforeSend": function(xhr, settings) {
                console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
                },
            "success": function(result) {
                if (result.dislikes) {
                    console.log("Post Disliked!" + MemeId);
                    console.log(result);

                    $('#dislike-' + MemeId).text(result.dislikes);

                    console.log("Got who Disliked! " + MemeId);
                    var result_dislikers = result.dislikers;
                    var actual_dislikers = "";

                    for (i = 0; i < result_dislikers.length; i++) {
                        actual_dislikers += result_dislikers[i].username + " ";
                    }
                    console.log(actual_dislikers);
                    $('#who_dislike-' + MemeId).text(actual_dislikers);
                } else {
                    console.log("No result for meme " + MemeId);
                    $('#dislike-' + MemeId).text(0);
                    $('#who_dislike-' + MemeId).text("");
                }
            },
        });
        // $.ajax({
        //     "type": "GET",
        //     "dataType": "json",
        //     contentType: "application/json; charset=utf-8",
        //     "url": "/ajax/memes/"+MemeId+"/likes/",
        //     "beforeSend": function(xhr, settings) {
        //         console.log("Before Send");
        //         $.ajaxSettings.beforeSend(xhr, settings);
        //         },
        //     "success": function(result) {
        //         if (result[0]){
        //             console.log("Got who disliked!"+MemeId);
        //             console.log(result);
        //             console.log(result[0].id);
        //             $('#who_disliked-'+MemeId).text(result.author);
        //         } else {
        //             console.log("No result for meme "+MemeId);
        //         }
        //     },
        // });
    });
});