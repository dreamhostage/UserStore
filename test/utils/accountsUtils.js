const accountsConfig = require('../../accounts-data/accounts.json');
const tronWeb = require('tronweb');

let accounts = [];

for (privateKey of accountsConfig.privateKeys) {
    const address = tronWeb.address.fromPrivateKey(privateKey);
    const hex = tronWeb.address.toHex(address);
    const account = {
        privateKey: privateKey,
        address: address,
        hex: hex,
    };
    accounts.push(account);
}

module.exports = {
    accounts: accounts,
};
