$(document).ready(function () {

    // FIXME Quotes?
    let cookie_protected_key = stripQuotes(getCookie("protected_key"));
    let cookie_iv = getCookie("iv");
    let iv = new ByteData(fromB64(cookie_iv));
    let protected_key = new ByteData(fromB64(cookie_protected_key));

    dbExecute(function (store) {

        let getData = store.get(1);
        getData.onsuccess = async function () {

            let masterKey = getData.result.masterKey;
            let decryptedKey = await decryptKey(masterKey, iv.array.buffer, protected_key.array.buffer);

            dbExecute(function (store) {
                store.put({id: 2, decryptedKey: decryptedKey});
            });
        };
        store.put({id: 3, iv: iv});
    });
});
