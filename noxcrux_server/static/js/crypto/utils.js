function UTF8toBytes(str) {

    const strUtf8 = unescape(encodeURIComponent(str));
    const bytes = new Uint8Array(strUtf8.length);

    for (let i = 0; i < strUtf8.length; i++)
        bytes[i] = strUtf8.charCodeAt(i);

    return bytes.buffer;
}

function bytesToUTF8(buffer) {

    const bytes = new Uint8Array(buffer);
    const encodedString = String.fromCharCode.apply(null, bytes);
    return decodeURIComponent(escape(encodedString));
}

function bytesToB64(buf) {

    let binary = '';
    const bytes = new Uint8Array(buf);

    for (let i = 0; i < bytes.byteLength; i++)
        binary += String.fromCharCode(bytes[i]);

    return window.btoa(binary);
}

function b64ToBytes(b64) {

    let raw = window.atob(b64);
    let array = new Uint8Array(new ArrayBuffer(raw.length));

    for (let i = 0; i < raw.length; i++)
        array[i] = raw.charCodeAt(i);

    return array;
}

async function pbkdf2(password, salt, iterations) {

    const algorithm = {
        name: 'PBKDF2',
    };

    const parameters = {
        name: 'PBKDF2',
        salt: salt.array.buffer,
        iterations: iterations,
        hash: {name: 'SHA-256'},
    };

    const usageOptions = {
        name: 'AES-GCM',
        length: 256,
    };

    try {

        const importedKey = await window.crypto.subtle.importKey('raw', password.array.buffer, algorithm, false, ['deriveKey']);
        const derivedKey = await window.crypto.subtle.deriveKey(parameters, importedKey, usageOptions, true, ['encrypt']);
        const exportedKey = await window.crypto.subtle.exportKey('raw', derivedKey);
        return new CryptoData(exportedKey);

    } catch (err) {

        console.log(err)
    }
}

async function generateRsaKeyPair() {

    const rsaOptions = {
        name: 'RSA-OAEP',
        modulusLength: 4096,
        publicExponent: new Uint8Array([0x01, 0x00, 0x01]), // 65537
        hash: {name: 'SHA-256'},
    };

    try {

        const keyPair = await window.crypto.subtle.generateKey(rsaOptions, true, ['encrypt', 'decrypt']);
        const publicKey = await window.crypto.subtle.exportKey('spki', keyPair.publicKey);
        const privateKey = await window.crypto.subtle.exportKey('pkcs8', keyPair.privateKey);

        return {
            publicKey: new CryptoData(publicKey),
            privateKey: new CryptoData(privateKey),
        };

    } catch (err) {

        console.error(err);
    }
}

async function encryptKey(masterKey, iv, privateKey) {

    const keyOptions = {
        name: 'AES-GCM',
        length: 256,
    }

    const aesOptions = {
        name: "AES-GCM",
        length: 256,
        iv: iv.array.buffer,
    };

    try {

        const importedKey = await window.crypto.subtle.importKey('raw', masterKey.array.buffer, keyOptions, false, ['encrypt']);
        let protected_key = await window.crypto.subtle.encrypt(aesOptions, importedKey, privateKey.array.buffer);
        return new CryptoData(protected_key);

    } catch (err) {

        console.error(err);
    }
}

async function decryptKey(masterKey, iv, protectedKey) {

    const keyOptions = {
        name: 'AES-GCM',
        length: 256,
    }

    const aesOptions = {
        name: "AES-GCM",
        length: 256,
        iv: iv.array.buffer,
    };

    try {

        const importedKey = await window.crypto.subtle.importKey('raw', masterKey.array.buffer, keyOptions, false, ['decrypt']);
        let privateKey = await window.crypto.subtle.decrypt(aesOptions, importedKey, protectedKey.array.buffer);
        return new CryptoData(privateKey);

    } catch (err) {

        console.error(err);
    }
}

async function encryptHorcrux(horcrux, publicKey) {

    const rsaOptions = {
        name: 'RSA-OAEP',
        modulusLength: 4096,
        publicExponent: new Uint8Array([0x01, 0x00, 0x01]), // 65537
        hash: {name: 'SHA-256'},
    };

    try {

        const importedKey = await window.crypto.subtle.importKey('spki', publicKey.array.buffer, rsaOptions, false, ['encrypt']);
        const encryptedHorcrux = await window.crypto.subtle.encrypt(rsaOptions, importedKey, horcrux.array.buffer);
        return new CryptoData(encryptedHorcrux);

    } catch (err) {

        console.error(err);
    }
}

async function decryptHorcrux(horcrux, protectedKey) {

    const rsaOptions = {
        name: 'RSA-OAEP',
        modulusLength: 4096,
        publicExponent: new Uint8Array([0x01, 0x00, 0x01]), // 65537
        hash: {name: 'SHA-256'},
    };

    try {

        const importedKey = await window.crypto.subtle.importKey('pkcs8', protectedKey.array.buffer, rsaOptions, false, ['decrypt']);
        const decryptedHorcrux = await window.crypto.subtle.decrypt(rsaOptions, importedKey, horcrux.array.buffer);
        return new CryptoData(decryptedHorcrux);

    } catch (err) {

        console.error(err);
    }
}
