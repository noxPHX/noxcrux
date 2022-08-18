function dbSetup() {

    return new Promise(function (resolve, reject) {

        let indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB || window.shimIndexedDB;

        if (!window.indexedDB)
            reject("Your browser doesn't support a stable version of IndexedDB.");

        let request = indexedDB.open("KeysContainer", 3);

        request.onerror = function () {
            reject("Something wrong happened while using IndexedDB.");
        };

        // Migrations
        request.onupgradeneeded = function (e) {
            let db = e.target.result;
            let store = db.createObjectStore("MyKeys", {keyPath: "id"});
        };

        request.onsuccess = function (e) {
            let db = e.target.result;
            let tx = db.transaction("MyKeys", "readwrite");
            let store = tx.objectStore("MyKeys");

            resolve(store);

            tx.oncomplete = function () {
                db.close();
            };
        }
    });
}

function requestDB(request) {

    return new Promise(function (resolve, reject) {
        request.onsuccess = r => resolve(request.result);
        request.onerror = reject;
    });
}
