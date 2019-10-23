// EXAMPLE HTML
// {# FORM LIKE POST #}
// <form method='post' id='liking'>{% csrf_token %}
//     {# <input type="hidden" value="13"/>#}
//     <input type='submit' value='Like'/>
// </form>
// <div id="liking">
//     <p><label>Liked:</label> <span id="likes"></span></p>
// </div>
//
// {# FORM DISLIKE POST #}
// <form method='post' id='disliking'>{% csrf_token %}
//     {# <input type="hidden" value="13"/>#}
//     <input type='submit' value='DisLike'/>
// </form>
// <div id="disliking">
//     <p><label>Disliked:</label> <span id="dislikes"></span></p>
// </div>

$(document).ready(function() {
    var meme = JSON.parse(document.getElementById('meme-data').textContent);

    $("#liking").click(function(e) {
        e.preventDefault();
        // var data = {
        //     'foo': 'bar'
        // };
        $.ajax({
            "type": "POST",
            "dataType": "json",
            "url": "/ajax/memes/"+meme.id+"/liking/",
            // "data": data,
            "beforeSend": function(xhr, settings) {
                console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
                },
            "success": function(result) {
                // console.log("Adding Like!");
                // console.log(result);
                $('#likes').text(result.likes);
            },
        });
    });
    $("#disliking").click(function(e) {
        e.preventDefault();
        // var data = {
        //     'foo': 'bar'
        // };
        $.ajax({
            "type": "POST",
            "dataType": "json",
            "url": "/ajax/memes/"+meme.id+"/disliking/",
            // "data": data,
            "beforeSend": function(xhr, settings) {
                // console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
                },
            "success": function(result) {
                console.log("Adding dislike!");
                console.log(result);
                $('#dislikes').text(result.dislikes);
            },
        });
    });
});