$(function() {
    $("#id_slug").unbind('change');
    $("#id_title").unbind('keyup');

    // Automatically update the slug when typing the title
    var slug_auto = $("#id_title").attr("value") == "";
    var slug = $("#id_slug").change(function() {
        if ($("#id_slug").attr("value") == "")
            slug_auto = true;
        else
            slug_auto = false;
    });
    $("#id_title").keyup(function() {
        if(slug_auto)
            slug.val(URLify(this.value, 64));
    });
});