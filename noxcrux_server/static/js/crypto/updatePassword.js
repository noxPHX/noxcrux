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

    let store = await dbSetup();
    let decryptedKey = (await requestDB(store.get(3))).decryptedKey;

    let protectedKey = await encryptKey(masterKey, iv, decryptedKey);

    $('input[name="protected_key"]').val(protectedKey.b64);
    $('input[name="old_password"]').val(oldMasterHash.b64);
    $('input[name="new_password1"]').val(masterHash.b64);
    $('input[name="new_password2"]').val(masterHash2.b64);

    $(this).off('submit');
    $(this).submit();
});
