class CryptoData {

    constructor(data, providedType) {

        if (!arguments.length) {

            this.array = null;
            this.b64 = null;
            return;
        }

        let type = providedType || getTypeOf(data);

        switch (type) {

            case 'string':

                let bytes = UTF8toBytes(data);
                this.array = new Uint8Array(bytes);
                this.b64 = bytesToB64(bytes);
                break;

            case 'base64':

                this.array = b64ToBytes(data);
                this.b64 = data;
                break;

            case 'arraybuffer':

                this.array = new Uint8Array(data);
                this.b64 = bytesToB64(data);
                break;

            case 'uint8array':

                this.array = data;
                this.b64 = bytesToB64(data);
                break;

            default:
                throw 'CryptoData: Invalid argument provided';
        }
    }
}
