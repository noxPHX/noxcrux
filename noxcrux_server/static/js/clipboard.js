$(".horcrux-copy").on('click', function () {
    try {
        navigator.clipboard.writeText($(this).text());
        $("#messages").append('<div class="alert-fixed"> <div class="alert alert-info alert-dismissible fade show me-3" role="alert"> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> Copied! </div> </div>')
    } catch {
        $("#messages").append('<div class="alert-fixed"> <div class="alert alert-warning alert-dismissible fade show me-3" role="alert"> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button> Clipboard access denied! Please copy manually </div> </div>')
    }
    timeOuts();
});
