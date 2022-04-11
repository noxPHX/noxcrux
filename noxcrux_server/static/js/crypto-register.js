$("form").on('submit', async function (e) {

    e.preventDefault()

    let masterPassword = fromUtf8($('input[name="password"]').val());
    let username = fromUtf8($('input[name="username"]').val());

    let masterKey = await pbkdf2(masterPassword, username, 100000, 256);
    console.log('Master Key');
    console.log(masterKey);

    let masterHash = await pbkdf2(fromUtf8(masterKey.b64), masterPassword, 30000, 256);
    console.log('Master Hash');
    console.log(masterHash);

    let keyPair = await generateRsaKeyPair();
    console.log('Key Pair');
    console.log(keyPair);

    let iv = window.crypto.getRandomValues(new Uint8Array(12))
    let protectedKey = await encryptKey(masterKey, iv, keyPair.privateKey);
    console.log('Protected Key');
    console.log(protectedKey);

    $(this).off('submit');
    $(this).submit();
});
