$(document).ready(function () {
    // Empty passwords fields to avoid confusion with the hashed password
    $('input[name="old_password"]').val("");
    $('input[name="new_password1"]').val("");
    $('input[name="new_password2"]').val("");
});

$("form").on('submit', async function (e) {

    e.preventDefault();

    let username = new CryptoData($("#id_username").val());

    let oldMasterPassword = new CryptoData($('input[name="old_password"]').val());
    let masterPassword = new CryptoData($('input[name="new_password1"]').val());
    let masterPassword2 = new CryptoData($('input[name="new_password2"]').val());

    let oldMasterKey = await pbkdf2(oldMasterPassword, username, 100000);
    let masterKey = await pbkdf2(masterPassword, username, 100000);
    let masterKey2 = await pbkdf2(masterPassword2, username, 100000);

    let oldMasterHash = await pbkdf2(oldMasterKey, oldMasterPassword, 30000);
    let masterHash = await pbkdf2(masterKey, masterPassword, 30000);
    let masterHash2 = await pbkdf2(masterKey2, masterPassword2, 30000);

    let iv = new CryptoData($("#id_iv").val(), 'base64');

    let oldProtectedKey = new CryptoData($('input[name="protected_key"]').val(), 'base64');

    // If the provided password is wrong, the decryption will fail
    try {

        let decryptedKey = await decryptProtectedKey(oldMasterKey, iv, oldProtectedKey);
        let newProtectedKey = await encryptKey(masterKey, iv, decryptedKey);
        $('input[name="protected_key"]').val(newProtectedKey.b64);
        $('input[name="old_password"]').val(oldMasterHash.b64);
        $('input[name="new_password1"]').val(masterHash.b64);
        $('input[name="new_password2"]').val(masterHash2.b64);

    } catch (err) {

        $('input[name="old_password"]').val(oldMasterHash.b64);
        $('input[name="new_password1"]').val(masterHash.b64);
        $('input[name="new_password2"]').val(masterHash2.b64);
    }

    $(this).off('submit');
    $(this).submit();
});
