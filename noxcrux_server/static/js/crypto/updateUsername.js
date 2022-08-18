$(document).ready(function () {
    // Empty password field to avoid confusion with the hashed password
    $('input[name="old_password"]').val("");
});

$("form").on('submit', async function (e) {

    e.preventDefault();

    let oldUsername = new CryptoData($("#id_username").val());
    let newUsername = new CryptoData($('input[name="username"]').val());

    let masterPassword = new CryptoData($('input[name="old_password"]').val());

    let oldMasterKey = await pbkdf2(masterPassword, oldUsername, 100000);
    let newMasterKey = await pbkdf2(masterPassword, newUsername, 100000);

    let oldMasterHash = await pbkdf2(oldMasterKey, masterPassword, 30000);
    let newMasterHash = await pbkdf2(newMasterKey, masterPassword, 30000);

    let iv = new CryptoData($("#id_iv").val(), 'base64');

    let oldProtectedKey = new CryptoData($('input[name="protected_key"]').val(), 'base64');

    // If the provided password is wrong, the decryption will fail
    try {

        let decryptedKey = await decryptProtectedKey(oldMasterKey, iv, oldProtectedKey);
        let newProtectedKey = await encryptKey(newMasterKey, iv, decryptedKey);

        $('input[name="protected_key"]').val(newProtectedKey.b64);
        $('input[name="old_password"]').val(oldMasterHash.b64);
        $('input[name="new_password"]').val(newMasterHash.b64);

    } catch (err) {

        $('input[name="old_password"]').val(oldMasterHash.b64);
        $('input[name="new_password"]').val(oldMasterHash.b64);
    }

    $(this).off('submit');
    $(this).submit();
});
