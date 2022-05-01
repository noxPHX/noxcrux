$(document).ready(function () {
    // Empty passwords fields to avoid confusion with the hashed password
    $('input[name="password"]').val("");
    $('input[name="password2"]').val("");
});

$("form").on('submit', async function (e) {

    e.preventDefault();

    let username = new CryptoData($('input[name="username"]').val());

    let masterPassword = new CryptoData($('input[name="password"]').val());
    let masterPassword2 = new CryptoData($('input[name="password2"]').val());

    let masterKey = await pbkdf2(masterPassword, username, 100000);
    let masterKey2 = await pbkdf2(masterPassword2, username, 100000);

    let masterHash = await pbkdf2(masterKey, masterPassword, 30000);
    let masterHash2 = await pbkdf2(masterKey2, masterPassword2, 30000);

    let keyPair = await generateRsaKeyPair();

    let iv = generateIV();
    let protectedKey = await encryptKey(masterKey, iv, keyPair.privateKey);

    $("#id_public_key").val(keyPair.publicKey.b64);
    $("#id_protected_key").val(protectedKey.b64);
    $("#id_iv").val(iv.b64);
    $('input[name="password"]').val(masterHash.b64);
    $('input[name="password2"]').val(masterHash2.b64);

    $(this).off('submit');
    $(this).submit();
});
