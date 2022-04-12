$("form").on('submit', async function (e) {

    e.preventDefault()

    let masterPassword = fromUtf8($('input[name="password"]').val());
    let username = fromUtf8($('input[name="username"]').val());

    let masterKey = await pbkdf2(masterPassword, username, 100000, 256);

    let masterHash = await pbkdf2(fromUtf8(masterKey.b64), masterPassword, 30000, 256);

    let keyPair = await generateRsaKeyPair();

    let iv = window.crypto.getRandomValues(new Uint8Array(12))
    let protectedKey = await encryptKey(masterKey, iv, keyPair.privateKey);

    $("#id_public_key").val(keyPair.publicKey.b64);
    $("#id_private_key").val(protectedKey.b64);
    $("#id_iv").val(new ByteData(iv).b64);

    $(this).off('submit');
    $(this).submit();
});
