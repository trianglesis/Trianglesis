// EXAMPLE HTML
// <div id="meme-data">
//  {{ MEME_JSON.data|json_script:"meme-data" }}
// {#             {{ MEME_JSON|json_script:"meme-data" }}#}
// </div>
//
// <p>Form get_meme</p>
// {# FORM GET post tittle #}
// <form method='post' id='get_meme'>{% csrf_token %}
//     <input type="hidden" id="memeid_var" name="memeid" value="{{MEME.id}}">
//     <input type='submit' value='Test button'/>
// </form>
// <div id="title_get_meme">
//     <p><label>Tittle:</label><span id="title_get_meme"></span></p>
// </div>

// https://stackoverflow.com/a/8483184/4915733
$(document).ready(function() {
    $("#get_meme").click(function(e) {
        e.preventDefault();

        var MemeId = document.getElementById("memeid_var").value;
        console.log("Set MemeId - " + MemeId);

        var meme = JSON.parse(document.getElementById('meme-data').textContent);
        console.log("Meme JSON - " + meme);
        console.log("Meme JSON - " + meme['id']);
        console.log("Meme JSON - " + meme["id"]);
        console.log("Meme JSON - " + meme.id);


        // // var meme = JSON.parse(element_data);
        // console.log("Set meme .isArray() - " + Array.isArray(meme));
        //
        // var meme_arr = Array(meme);
        // console.log("Set meme .isArray() - " + Array.isArray(meme_arr));
        // console.log("Meme ARray meme_arr[0] - " + Array(meme_arr)[0]);
        // console.log("Meme ARray meme_arr[0]['pk'] - " + Array(meme_arr)[0]['pk']);
        // console.log("Meme ARray meme_arr[0][\"pk\"] - " + Array(meme_arr)[0]["pk"]);
        // console.log("Meme ARray meme_arr[0].pk - " + Array(meme_arr)[0].pk);

        $.ajax({
            "type": "GET",
            "dataType": "json",
            "url": "/ajax/memes/"+MemeId,
            // "data": data,
            "success": function(result) {
                console.log(result);
                $('#title_get_meme').text(result.title);
            },
        });
    });
});