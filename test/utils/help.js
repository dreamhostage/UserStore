const ADDRESS_PREFIX = '41';

function hexStringToBase58(sHexString) {
    if (sHexString.length < 2 || (sHexString.length & 1) != 0) return '';

    const bytes = tronWeb.utils.code.hexStr2byteArray(sHexString);
    return tronWeb.utils.crypto.getBase58CheckAddress(bytes);
}

function base58ToHexString(sBase58) {
    const bytes = tronWeb.utils.crypto.decodeBase58Address(sBase58);
    return tronWeb.utils.crypto.byteArray2hexStr(bytes);
}

function hexStringToUtf8(hex) {
    const arr = hex.split('');
    let out = '';

    for (let i = 0; i < arr.length / 2; i++) {
        const tmp = `0x${arr[i * 2]}${arr[i * 2 + 1]}`;
        const charValue = String.fromCharCode(tmp);
        out += charValue;
    }

    return out;
}

function stringUtf8tHex(str) {
    let val = '';

    for (let i = 0; i < str.length; i++) {
        if (val == '') val = str.charCodeAt(i).toString(16);
        else val += str.charCodeAt(i).toString(16);
    }

    return val;
}

function address2HexString(sHexAddress) {
    if (sHexAddress.length == 42 && sHexAddress.indexOf(ADDRESS_PREFIX) == 0)
        return sHexAddress;

    return base58ToHexString(sHexAddress);
}

function hexString2Address(sAddress) {
    return hexStringToBase58(sAddress);
}

function hexString2Utf8(sHexString) {
    return hexStringToUtf8(sHexString);
}

function stringUtf8toHex(sUtf8) {
    return stringUtf8tHex(sUtf8);
}

module.exports = {
    hexStringToBase58,
    hexStringToUtf8,
    stringUtf8tHex,
    address2HexString,
    hexString2Address,
    hexString2Utf8,
    stringUtf8toHex,
};
