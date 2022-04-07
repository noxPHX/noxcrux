class ByteData {

    constructor(buf) {

        if (!arguments.length) {

            this.arr = null;
            this.b64 = null;
            return;
        }

        this.arr = new Uint8Array(buf);
        this.b64 = toB64(buf);
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

async function pbkdf2(password, salt, iterations, length) {

    const algorithm = {
        name: 'PBKDF2',
    };

    const parameters = {
        name: 'PBKDF2',
        salt: salt,
        iterations: iterations,
        hash: {name: 'SHA-256'},
    };

    const aesOptions = {
        name: 'AES-CBC',
        length: length,
    };

    try {

        const importedKey = await window.crypto.subtle.importKey('raw', password, algorithm, false, ['deriveKey']);
        const derivedKey = await window.crypto.subtle.deriveKey(parameters, importedKey, aesOptions, true, ['encrypt']);
        const exportedKey = await window.crypto.subtle.exportKey('raw', derivedKey);
        return new ByteData(exportedKey);

    } catch (err) {

        console.log(err)
    }
}

$("form").on('submit', async function (e) {

    e.preventDefault();

    let password = fromUtf8($('input[name="password"]').val());
    let username = fromUtf8($('input[name="username"]').val());

    let master_key = await pbkdf2(password, username, 100000, 256);
    console.log(master_key);

    let master_hash = await pbkdf2(fromUtf8(master_key.b64), password, 30000, 256);
    console.log(master_hash);
});
