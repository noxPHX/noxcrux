$(document).ready(async function () {

    if (!getCookie("keys"))
        return

    // FIXME Quotes?
    let cookie_public_key = stripQuotes(getCookie("public_key"));
    let public_key = new CryptoData(b64ToBytes(cookie_public_key));
    let cookie_protected_key = stripQuotes(getCookie("protected_key"));
    let protected_key = new CryptoData(b64ToBytes(cookie_protected_key));
    let cookie_iv = getCookie("iv");
    let iv = new CryptoData(b64ToBytes(cookie_iv));

    dbSetup().then(function (store) {

        let getData = store.get(1);
        store.put({id: 2, publicKey: public_key});
        getData.onsuccess = async function () {

            let masterKey = getData.result.masterKey;
            let decryptedKey = await decryptKey(masterKey, iv.array.buffer, protected_key.array.buffer);

            dbSetup().then(function (store) {
                store.put({id: 3, decryptedKey: decryptedKey});
            });
        };
        store.put({id: 4, iv: iv});
    });
});
