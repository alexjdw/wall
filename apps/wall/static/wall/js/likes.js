$(document).ready(function() {
    $('.plike').click(function(e) {
        e.preventDefault();
        var post_id = $(this).attr('pid');
        $.ajax({
            url: "like-post/" + post_id,
            method: "GET",
        }).done(function() {
            return;
        });
    });
});