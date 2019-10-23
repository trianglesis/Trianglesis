// https://hackernoon.com/consume-rest-services-with-ajax-and-csrf-protection-in-django-410ece54690
// https://codeguida.com/post/470
// $(document).on('click', function() {
$(document).ready(function() {
    var data = $('#form').serialize();
    // var MemeId = document.getElementById("memeID").value;

    // $("#liking_"+MemeId).click(function(e) {
    // $("#liking_"+MemeId).on('click', '.like-button', function(e) {
    // $("#btn-liking-"+MemeId).on('click', function() {
    $(".like-button").on('click', function(e) {
        e.preventDefault();

        var $this = $(this);
        var MemeId = $this.attr('value');
        console.log("var id = " + MemeId);

        console.log("Set MemeId to Like - " + MemeId);
        console.log("Form data - " + data);
        $.ajax({
            "type": "POST",
            "dataType": "json",
            contentType: "application/json; charset=utf-8",
            "url": "/ajax/memes/"+MemeId+"/liking/",
            "data": data,
            "beforeSend": function(xhr, settings) {
                console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
                },
            "success": function(result) {
                console.log("Adding Like!");
                console.log(result);
                $('#likes').text(result.likes);
            },
        });
    });

    // $("#disliking_"+MemeId).click(function(e) {
    // $("#disliking_"+MemeId).on('click', '.dislike-button', function(e) {
    // $("#btn-disliking-"+MemeId).on('click', function() {
    $(".dislike-button").on('click', function(e) {
        e.preventDefault();

        var $this = $(this);
        var MemeId = $this.attr('value');
        console.log("var id = " + MemeId);

        console.log("Set MemeId to Dislike - " + MemeId);
        console.log("Form data - " + data);
        $.ajax({
            "type": "POST",
            "dataType": "json",
            contentType: "application/json; charset=utf-8",
            "url": "/ajax/memes/"+MemeId+"/disliking/",
            "data": data,
            "beforeSend": function(xhr, settings) {
                console.log("Before Send");
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