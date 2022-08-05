$("form").on('submit', function (e) {

    e.preventDefault();

    let form = $(this);

    $.ajax({
        method: 'GET',
        url: $(this).data('url') + $(this).find(":selected").text()
    })
        .done(async function (data) {

            let horcrux = new CryptoData($(".horcrux-copy").children("div").data("value"), 'base64');

            let store = await dbSetup();
            let storedKey = (await requestDB(store.get(3))).storedKey;
            let decryptedHorcrux = await decryptHorcrux(horcrux, storedKey);
            let encryptedHorcrux = await encryptHorcrux(decryptedHorcrux, new CryptoData(data.public_key, 'base64'));
            $('input[name="shared_horcrux"]').val(encryptedHorcrux.b64);
            form.off('submit');
            form.submit();
        });
});
