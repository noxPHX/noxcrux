$(".horcrux-copy").on('click', async function () {

    let horcrux = fromB64($(this).children("div").data("value"));

    let store = await dbSetup();
    let object = await requestDB(store.get(3));
    let decryptedHorcrux = await decryptHorcrux(horcrux, object.decryptedKey);
    $(this).children("div").html(toUtf8(decryptedHorcrux));

    try {
        await navigator.clipboard.writeText($(this).find(".card-text").text());
        $("#messages").append('<div class="alert alert-info alert-dismissible fade show" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' + $(this).find(".card-text").data('name') + ' horcrux copied!</div>')
    } catch {
        $("#messages").append('<div class="alert alert-warning alert-dismissible fade show" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Clipboard access denied! Please copy manually</div>')
    }
    timeOuts();
});
