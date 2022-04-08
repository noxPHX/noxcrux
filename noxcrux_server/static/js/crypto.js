class ByteData {

    constructor(data) {

        if (!arguments.length) {

            this.array = null;
            this.b64 = null;
            return;
        }

        this.array = new Uint8Array(data);
        this.b64 = toB64(data);
    }
}

function fromUtf8(str) {

    const strUtf8 = unescape(encodeURIComponent(str));
    const bytes = new Uint8Array(strUtf8.length);

    for (let i = 0; i < strUtf8.length; i++)
        bytes[i] = strUtf8.charCodeAt(i);

    return bytes.buffer;
}

function toUtf8(buf) {

    const bytes = new Uint8Array(buf);
    const encodedString = String.fromCharCode.apply(null, bytes);
    return decodeURIComponent(escape(encodedString));
}

function toB64(buf) {

    let binary = '';
    const bytes = new Uint8Array(buf);

    for (let i = 0; i < bytes.byteLength; i++)
        binary += String.fromCharCode(bytes[i]);

    return window.btoa(binary);
}

async function pbkdf2(password, salt, iterations) {

    const algorithm = {
        name: 'PBKDF2',
    };

    const parameters = {
        name: 'PBKDF2',
        salt: salt,
        iterations: iterations,
        hash: {name: 'SHA-256'},
    };

    const usageOptions = {
        name: 'AES-GCM',
        length: 256,
    };

    try {

        const importedKey = await window.crypto.subtle.importKey('raw', password, algorithm, false, ['deriveKey']);
        const derivedKey = await window.crypto.subtle.deriveKey(parameters, importedKey, usageOptions, true, ['encrypt']);
        const exportedKey = await window.crypto.subtle.exportKey('raw', derivedKey);
        return new ByteData(exportedKey);

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
            publicKey: new ByteData(publicKey),
            privateKey: new ByteData(privateKey),
        };

    } catch (err) {

        console.error(err);
    }
}

async function encryptMessage(key, iv, message) {

    const keyOptions = {
        name: 'AES-GCM',
    }

    const aesOptions = {
        name: "AES-GCM",
        iv: iv,
    };

    const importedKey = await window.crypto.subtle.importKey('raw', key.array.buffer, keyOptions, false, ['encrypt'])
    return await window.crypto.subtle.encrypt(aesOptions, importedKey, message.array.buffer);
}

async function decryptMessage(key, iv, message) {

    const keyOptions = {
        name: 'AES-GCM',
    }

    const aesOptions = {
        name: "AES-GCM",
        iv: iv,
    };

    const importedKey = await window.crypto.subtle.importKey('raw', key.array.buffer, keyOptions, false, ['decrypt'])
    return await window.crypto.subtle.decrypt(aesOptions, importedKey, message);
}

$("form").on('submit', async function (e) {

    e.preventDefault();

    let master_password = fromUtf8($('input[name="password"]').val());
    let username = fromUtf8($('input[name="username"]').val());

    let master_key = await pbkdf2(master_password, username, 100000, 256);
    console.log('Master Key');
    console.log(master_key);

    let master_hash = await pbkdf2(fromUtf8(master_key.b64), master_password, 30000, 256);
    console.log('Master Hash');
    console.log(master_hash);

    //const keys = nacl.box.keyPair();
    //let public_key = new ByteData(keys.publicKey);
    //let private_key = new ByteData(keys.secretKey);
    let keys = await generateRsaKeyPair();
    console.log('Key Pair');
    console.log(keys);

    let iv = window.crypto.getRandomValues(new Uint8Array(12))
    let protected_key = await encryptMessage(master_key, iv, keys.privateKey);
    console.log('Protected Key');
    console.log(protected_key);

    let decrypted_key = await decryptMessage(master_key, iv, protected_key);
    console.log('Decrypted Key');
    console.log(new ByteData(decrypted_key));
});
