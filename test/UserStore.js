const UserStore = artifacts.require('./UserStore.sol');
const assert = require('assert');
const { accounts } = require('./utils/accountsUtils');

contract('UserStore', function () {
    let contractInstance;
    let contractAddress;
    
    beforeEach(async () => {
        const newContract = await UserStore.new();
        contractInstance = await tronWeb.contract().at(newContract.address);
        contractAddress = newContract.address;
    });

    it('Is deployed successfully', function () {
        assert(contractInstance);
    });

    it('Add and get data using key', async () => {

        const userAddress = accounts[0];
        let key = "key value";
        let data = "Data value"; 

        let [txId, output] = await contractInstance
            .mintToken(key, data)
            .send(
                {
                    shouldPollResponse: true,
                    keepTxID: true,
                },
                (privateKey = userAddress.privateKey)
            );
        
        try {res = await contractInstance.getTokenData(key).call({ from: userAddress.hex });}
        catch (error) {console.log(error);}

        assert.strictEqual(res, data, 'Expected receiving of stored data.');
    });

    it('Get data by wrong key value', async () => {

        const userAddress = accounts[0];
        let key = "key value";
        let wrongKey = "wrong key value";
        let data = "Data value";
        let errorInfo = "";
        let expectedErrorInfo = "REVERT opcode executed";

        let [txId, output] = await contractInstance
            .mintToken(key, data)
            .send(
                {
                    shouldPollResponse: true,
                    keepTxID: true,
                },
                (privateKey = userAddress.privateKey)
            );
        
        try {res = await contractInstance.getTokenData(wrongKey).call({ from: userAddress.hex });}
        catch (error) {
            errorInfo = error;
        }

        assert.notStrictEqual(data, res, 'Expected no token data.');
    });

    it('Let transfer key to another address', async () => {

        const userAddress = accounts[0];
        const anotherAddress = accounts[1];
        let key = "key value";
        let data = "Data value";
        let errorInfo = "";
        let expectedErrorInfo = "REVERT opcode executed";

        await contractInstance
            .mintToken(key, data)
            .send(
                {
                    shouldPollResponse: true,
                    keepTxID: true,
                },
                (privateKey = userAddress.privateKey)
            );

        try {res = await contractInstance.getTokenOwner(key).call({ from: userAddress.hex });}
        catch (error) {console.log(error);}

        assert.strictEqual(res, userAddress.hex, 'Expected receiving token address owner.');

        await contractInstance
            .transferToken(key, anotherAddress.address)
            .send(
                {
                    shouldPollResponse: true,
                    keepTxID: true,
                },
                (privateKey = userAddress.privateKey)
            );

        try {res = await contractInstance.getTokenOwner(key).call({ from: userAddress.hex });}
        catch (error) {console.log(error);}
        
        assert.strictEqual(res, anotherAddress.hex, 'Expected receiving token address owner.');
    });

});
