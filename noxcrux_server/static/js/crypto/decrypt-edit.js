$(document).ready(async function () {

    let horcrux = new CryptoData($('input[name=horcrux]').val(), 'base64');

    let store = await dbSetup();
    let storedKey = (await requestDB(store.get(3))).storedKey;
    let decryptedHorcrux = await decryptHorcrux(horcrux, storedKey);
    $('input[name=horcrux]').val(bytesToUTF8(decryptedHorcrux.array.buffer));
});
