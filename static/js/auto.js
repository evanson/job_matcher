$(document).ready(function() {
    var opts = {
        lines: 17, // The number of lines to draw
        length: 0, // The length of each line
        width: 60, // The line thickness
        radius: 120, // The radius of the inner circle
        corners: 1, // Corner roundness (0..1)
        rotate: 90, // The rotation offset
        direction: 1, // 1: clockwise, -1: counterclockwise
        color: '#000', // #rgb or #rrggbb or array of colors
        speed: 1.5, // Rounds per second
        trail: 100, // Afterglow percentage
        shadow: false, // Whether to render a shadow
        hwaccel: false, // Whether to use hardware acceleration
        className: 'spinner', // The CSS class to assign to the spinner
        zIndex: 2e9, // The z-index (defaults to 2000000000)
        top: '50%', // Top position relative to parent
        left: '50%' // Left position relative to parent
        
    };
    $('#assist').click(function(e) {
        //$(this).attr('disabled', 'disabled')
        e.preventDefault();
        var url = $(this).attr('href');
        var spinner = new Spinner(opts).spin($('#profile')[0]);
        $.get(
            url,
            function(data) {
                bootbox.dialog({
                    //title: "Details",
                    message: data,
                });
                spinner.stop()
            }
        );
    });
    $('.close').click(function(e) {
        bootbox.hideAll();
    });
    $("#assistmsg").hide();

});
