/**
 * Used by CryptoData to convert a string into bytes
 * @param str Usually a string provided by the user
 * @returns {ArrayBufferLike}
 */
function UTF8toBytes(str) {

    const strUtf8 = unescape(encodeURIComponent(str));
    const bytes = new Uint8Array(strUtf8.length);

    for (let i = 0; i < strUtf8.length; i++)
        bytes[i] = strUtf8.charCodeAt(i);

    return bytes.buffer;
}

/**
 * Used to convert a CryptoData (horcrux) into plain text
 * @param buffer CryptoData (horcrux) buffer
 * @returns {string}
 */
function bytesToUTF8(buffer) {

    const bytes = new Uint8Array(buffer);
    const encodedString = String.fromCharCode.apply(null, bytes);
    return decodeURIComponent(escape(encodedString));
}

/**
 * Used by CryptoData to convert bytes into a base 64 encoded string
 * @param buf A bytes array
 * @returns {string}
 */
function bytesToB64(buf) {

    let binary = '';
    const bytes = new Uint8Array(buf);

    for (let i = 0; i < bytes.byteLength; i++)
        binary += String.fromCharCode(bytes[i]);

    return window.btoa(binary);
}

/**
 * Used by CryptoData to convert a base 64 string into bytes
 * @param b64 The base 64 encoded string
 * @returns {Uint8Array}
 */
function b64ToBytes(b64) {

    let raw = window.atob(b64);
    let array = new Uint8Array(new ArrayBuffer(raw.length));

    for (let i = 0; i < raw.length; i++)
        array[i] = raw.charCodeAt(i);

    return array;
}

/**
 * Function to derive / hash a payload
 * @param password A CryptoData object containing the payload to derive
 * @param salt A CryptoData object containing the salt
 * @param iterations The number of iterations to feed to the pbkdf2 function
 * @returns {CryptoData}
 */
async function pbkdf2(password, salt, iterations) {

    try {

        const importedKey = await window.crypto.subtle.importKey('raw', password.array.buffer, CryptoOptions.PBKDF2, false, ['deriveKey']);
        const derivedKey = await window.crypto.subtle.deriveKey(CryptoOptions.fPBKDF2(salt, iterations), importedKey, CryptoOptions.AES, true, ['encrypt']);
        const exportedKey = await window.crypto.subtle.exportKey('raw', derivedKey);
        return new CryptoData(exportedKey);

    } catch (err) {

        console.log(err)
    }
}

/**
 * Generates and returns an RSA-OEAP 4096 key pair
 * @returns {privateKey: CryptoData, publicKey: CryptoData}
 */
async function generateRsaKeyPair() {

    try {

        const keyPair = await window.crypto.subtle.generateKey(CryptoOptions.RSA, true, ['encrypt', 'decrypt']);
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

/**
 * Generates and returns an Initialization Vector to use with AES encryption
 * @returns {CryptoData}
 */
function generateIV() {

    let iv = window.crypto.getRandomValues(new Uint8Array(12));
    return new CryptoData(iv);
}

/**
 * Function to encrypt the user's private key
 * @param masterKey A CryptoData object containing the Master Key
 * @param iv A CryptoData object containing the IV
 * @param privateKey A CryptoData object containing the private key to encrypt
 * @returns {CryptoData}
 */
async function encryptKey(masterKey, iv, privateKey) {

    try {

        const importedKey = await window.crypto.subtle.importKey('raw', masterKey.array.buffer, CryptoOptions.AES, false, ['encrypt']);
        let protected_key = await window.crypto.subtle.encrypt(CryptoOptions.fAES(iv), importedKey, privateKey.array.buffer);
        return new CryptoData(protected_key);

    } catch (err) {

        console.error(err);
    }
}

/**
 * Function to decrypt the user's protected key
 * @param masterKey A CryptoData object containing the Master Key
 * @param iv A CryptoData object containing the IV
 * @param protectedKey A CryptoData object containing the Protected Key
 * @returns {CryptoKey}
 */
async function decryptKey(masterKey, iv, protectedKey) {

    try {

        const importedKey = await window.crypto.subtle.importKey('raw', masterKey.array.buffer, CryptoOptions.AES, false, ['decrypt']);
        let privateKey = await window.crypto.subtle.decrypt(CryptoOptions.fAES(iv), importedKey, protectedKey.array.buffer);
        return await window.crypto.subtle.importKey('pkcs8', privateKey, CryptoOptions.RSA, false, ['decrypt']);

    } catch (err) {

        console.error(err);
    }
}

/**
 * Function to decrypt the user's protected key
 * @param masterKey A CryptoData object containing the Master Key
 * @param iv A CryptoData object containing the IV
 * @param protectedKey A CryptoData object containing the Protected Key
 * @returns {CryptoData}
 */
async function decryptProtectedKey(masterKey, iv, protectedKey) {

    try {

        const importedKey = await window.crypto.subtle.importKey('raw', masterKey.array.buffer, CryptoOptions.AES, false, ['decrypt']);
        let privateKey = await window.crypto.subtle.decrypt(CryptoOptions.fAES(iv), importedKey, protectedKey.array.buffer);
        return new CryptoData(privateKey);

    } catch (err) {

        console.error(err);
    }
}

/**
 * Function used to encrypt an horcrux
 * @param horcrux A CryptoData object containing the horcrux to encrypt
 * @param publicKey A CryptoData object containing the public key
 * @returns {CryptoData}
 */
async function encryptHorcrux(horcrux, publicKey) {

    try {

        const importedKey = await window.crypto.subtle.importKey('spki', publicKey.array.buffer, CryptoOptions.RSA, false, ['encrypt']);
        const encryptedHorcrux = await window.crypto.subtle.encrypt(CryptoOptions.RSA, importedKey, horcrux.array.buffer);
        return new CryptoData(encryptedHorcrux);

    } catch (err) {

        console.error(err);
    }
}

/**
 * Function used to decrypt an horcrux
 * @param horcrux A CryptoData object containing the encrypted horcrux
 * @param storedKey A CryptoKey object containing the user's private key
 * @returns {CryptoData}
 */
async function decryptHorcrux(horcrux, storedKey) {

    try {

        const decryptedHorcrux = await window.crypto.subtle.decrypt(CryptoOptions.RSA, storedKey, horcrux.array.buffer);
        return new CryptoData(decryptedHorcrux);

    } catch (err) {

        console.error(err);
    }
}
