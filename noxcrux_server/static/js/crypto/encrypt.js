$("form").on('submit', async function (e) {

    e.preventDefault();

    let horcrux = new CryptoData($('input[name="horcrux"]').val());

    let store = await dbSetup();
    let publicKey = (await requestDB(store.get(2))).publicKey;
    let encryptedHorcrux = await encryptHorcrux(horcrux, publicKey);
    $('input[name="horcrux"]').val(encryptedHorcrux.b64);
    $(this).off('submit');
    $(this).submit();
});
