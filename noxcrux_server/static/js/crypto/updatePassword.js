$(document).ready(function () {
    // Empty passwords fields to avoid confusion with the hashed password
    $('input[name="old_password"]').val("");
    $('input[name="new_password1"]').val("");
    $('input[name="new_password2"]').val("");
});

$("form").on('submit', async function (e) {

    e.preventDefault();

    let username = UTF8toBytes($("#id_username").val());

    let oldMasterPassword = UTF8toBytes($('input[name="old_password"]').val());
    let masterPassword = UTF8toBytes($('input[name="new_password1"]').val());
    let masterPassword2 = UTF8toBytes($('input[name="new_password2"]').val());

    let oldMasterKey = await pbkdf2(oldMasterPassword, username, 100000);
    let masterKey = await pbkdf2(masterPassword, username, 100000);
    let masterKey2 = await pbkdf2(masterPassword2, username, 100000);

    let oldMasterHash = await pbkdf2(oldMasterKey.array.buffer, oldMasterPassword, 30000);
    let masterHash = await pbkdf2(masterKey.array.buffer, masterPassword, 30000);
    let masterHash2 = await pbkdf2(masterKey2.array.buffer, masterPassword2, 30000);

    let iv = new CryptoData(b64ToBytes($("#id_iv").val()));

    let store = await dbSetup();
    let object = await requestDB(store.get(3));

    let protectedKey = await encryptKey(masterKey, iv.array.buffer, object.decryptedKey);

    $('input[name="protected_key"]').val(protectedKey.b64);
    $('input[name="old_password"]').val(oldMasterHash.b64);
    $('input[name="new_password1"]').val(masterHash.b64);
    $('input[name="new_password2"]').val(masterHash2.b64);

    $(this).off('submit');
    $(this).submit();
});
