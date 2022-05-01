$("#id_submit").on('click', async function () {

    let username = new CryptoData($('input[name="username"]').val());
    let masterPassword = new CryptoData($('input[name="password"]').val());

    let masterKey = await pbkdf2(masterPassword, username, 100000);
    $("#id_master_key").val(masterKey.b64);

    let masterHash = await pbkdf2(masterKey, masterPassword, 30000);
    $("#id_master_hash").val(masterHash.b64);

    let keyPair = await generateRsaKeyPair();
    $("#id_public_key").val(keyPair.publicKey.b64);
    $("#id_private_key").val(keyPair.privateKey.b64);

    let iv = generateIV();
    $("#id_iv").val(iv.b64);

    let protectedKey = await encryptKey(masterKey, iv, keyPair.privateKey);
    $("#id_protected_key").val(protectedKey.b64);

    $("#id_encrypt").on('click', async function () {

        let horcrux = new CryptoData($("#id_plain").val());
        let encryptedHorcrux = await encryptHorcrux(horcrux, keyPair.publicKey);
        $("#id_cipher").val(encryptedHorcrux.b64);

        let decryptedHorcrux = await decryptHorcrux(encryptedHorcrux, keyPair.privateKey);
        $("#id_decrypted").val(bytesToUTF8(decryptedHorcrux.array.buffer));
    });
});
