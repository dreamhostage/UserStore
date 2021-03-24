const { address2HexString, hexString2Address } = require('./help');

const sleep = (ms) => {
    return new Promise((resolve) => setTimeout(resolve, ms));
};

const waitForNextBlock = async () => {
    await sleep(4000);
};

const catchEvent = async (contractInstance, eventName) => {
    return new Promise(async (resolve, reject) => {
        let eventCaught = false;
        const eventListener = await contractInstance[eventName]().watch(
            (err, eventResult) => {
                if (err) {
                    eventCaught = true;
                    reject(err);
                    return;
                }
                if (eventResult) {
                    eventCaught = true;
                    resolve(eventResult);
                }
            }
        );

        let timerId = setTimeout(
            function tick(elapsed) {
                if (eventCaught) {
                    eventListener.stop();
                } else {
                    if (elapsed > 10000) {
                        reject('Timeout');
                    } else {
                        timerId = setTimeout(tick, 1000, elapsed + 1000);
                    }
                }
            },
            2000,
            2000
        );
    });
};

const checkEventInTx = async (contractAddress, eventName, txId) => {
    let events = await tronWeb.event.getEventsByTransactionID(txId);
    let address = hexString2Address(address2HexString(contractAddress)); // hex address 2 hex is no-op
    let filteredEvents = [];
    for (event of events) {
        if (event.contract == address && event.name == eventName) {
            // not hex address!
            filteredEvents.push(event);
        }
    }
    return filteredEvents;
};

module.exports = {
    sleep,
    waitForNextBlock,
    catchEvent,
    checkEventInTx,
};
