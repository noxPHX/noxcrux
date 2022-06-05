class CryptoOptions {

    static PBKDF2 = {
        name: 'PBKDF2',
    }

    static fPBKDF2(salt, iterations) {
        return {
            ...CryptoOptions.PBKDF2,
            salt: salt.array.buffer,
            iterations: iterations,
            hash: {name: 'SHA-256'},
        }
    }

    static AES = {
        name: 'AES-GCM',
        length: 256,
    }

    static fAES(iv) {
        return {
            ...CryptoOptions.AES,
            iv: iv.array.buffer,
        }
    }

    static RSA = {
        name: 'RSA-OAEP',
        modulusLength: 4096,
        publicExponent: new Uint8Array([0x01, 0x00, 0x01]), // 65537
        hash: {name: 'SHA-256'},
    }
}
