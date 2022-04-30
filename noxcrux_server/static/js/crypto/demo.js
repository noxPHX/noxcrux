$("#id_submit").on('click', async function () {

    let username = fromUtf8($('input[name="username"]').val());
    let masterPassword = fromUtf8($('input[name="password"]').val());

    let masterKey = await pbkdf2(masterPassword, username, 100000);
    $("#id_master_key").val(masterKey.b64);

    let masterHash = await pbkdf2(masterKey.array.buffer, masterPassword, 30000);
    $("#id_master_hash").val(masterHash.b64);

    let keyPair = await generateRsaKeyPair();
    $("#id_public_key").val(keyPair.publicKey.b64);
    $("#id_private_key").val(keyPair.privateKey.b64);

    let iv = window.crypto.getRandomValues(new Uint8Array(12));
    $("#id_iv").val(new ByteData(iv).b64);

    let protectedKey = await encryptKey(masterKey, iv, keyPair.privateKey);
    $("#id_protected_key").val(protectedKey.b64);

    $("#id_encrypt").on('click', async function () {

        let horcrux = fromUtf8($("#id_plain").val());
        let encryptedHorcrux = await encryptHorcrux(horcrux, keyPair.publicKey);
        $("#id_cipher").val(encryptedHorcrux.b64);

        let decryptedHorcrux = await decryptHorcrux(encryptedHorcrux.array.buffer, keyPair.privateKey);
        $("#id_decrypted").val(toUtf8(decryptedHorcrux));
    });
});
