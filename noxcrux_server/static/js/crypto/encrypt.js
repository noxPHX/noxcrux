$("form").on('submit', async function (e) {

    e.preventDefault();

    let horcrux = new CryptoData($('input[name="horcrux"]').val());

    let store = await dbSetup();
    let object = await requestDB(store.get(2));
    let encryptedHorcrux = await encryptHorcrux(horcrux, object.publicKey);
    $('input[name="horcrux"]').val(encryptedHorcrux.b64);
    $(this).off('submit');
    $(this).submit();
});
