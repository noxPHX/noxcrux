$(document).ready(async function () {

    // FIXME Quotes?
    let cookie_protected_key = stripQuotes(getCookie("protected_key"));
    let cookie_iv = getCookie("iv");

    let masterKey = new ByteData(fromB64(sessionStorage.getItem("masterKey")));
    let iv = new ByteData(fromB64(cookie_iv));

    let protected_key = new ByteData(fromB64(cookie_protected_key));

    let decryptedKey = await decryptKey(masterKey, iv.array.buffer, protected_key.array.buffer);
    // sessionStorage.setItem("decryptedKey", decryptedKey.b64)
});
