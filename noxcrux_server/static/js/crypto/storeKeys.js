$(document).ready(async function () {

    if (!getCookie("keys"))
        return

    // FIXME Quotes?
    let public_key = new CryptoData(stripQuotes(getCookie("public_key")), 'base64');
    let protected_key = new CryptoData(stripQuotes(getCookie("protected_key")), 'base64');
    let iv = new CryptoData(stripQuotes(getCookie("iv")), 'base64');

    dbSetup().then(function (store) {

        let getData = store.get(1);
        store.put({id: 2, publicKey: public_key});
        getData.onsuccess = async function () {

            let masterKey = getData.result.masterKey;
            let decryptedKey = await decryptKey(masterKey, iv, protected_key);

            dbSetup().then(function (store) {
                store.put({id: 3, decryptedKey: decryptedKey});
            });
        };
        store.put({id: 4, iv: iv});
    });
});
