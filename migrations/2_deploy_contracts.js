const UserStore = artifacts.require('./UserStore.sol');

async function setupContracts(deployer, network) {
    console.log('Deploying UserStore...');

    await deployer.deploy(UserStore);
    let UserStoreInstance = await UserStore.deployed();
}

module.exports = function (deployer, network) {
    deployer.then(async () => await setupContracts(deployer, network));
};
