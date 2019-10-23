$('#get_meme_ex').click(function(){
    var memeid = $(this).attr("data-meme_id");
    console.log("Set catid - " + memeid);
    var username = $(this).val();
    console.log("Set username - " + username);
    $.get('/ajax/memes/'+memeid, function(data){
        $('#title').html(data);
        $('#title_get_meme_ex').html(data);
    });
});