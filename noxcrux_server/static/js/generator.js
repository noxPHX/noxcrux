$("#copy-generated").on('click', function () {
    try {
        navigator.clipboard.writeText($(this).parent('form').find("input[name='generated']").val());
        $("#messages").append('<div class="alert alert-info alert-dismissible fade show" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Horcrux copied!</div>')
    } catch {
        $("#messages").append('<div class="alert alert-warning alert-dismissible fade show" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Clipboard access denied! Please copy manually</div>')
    }
    timeOuts();
});
