# UserStore
Smart contract is deploy into the Tron network. For interacting use API implemented on native python Tron SDK. Tests was written on JavaScript using TronWeb library.
Smart contract is able to mint unique Token and assign it to ownable of any user. User also is able to transfer ownable of Token. Every Token has string data which can be accessed by key.

Install tronbox and npm dependencies:
```
sudo npm install -g tronbox
docker pull trontools/quickstart
```
Now we have to run tron node for development purposes. To run the contrainer use:
```
docker run -it -p 9090:9090 -v $PWD/accounts-data:/config --rm --name tron -e "accounts=1" -e "defaultBalance=2000000000" trontools/quickstart
```
Deploy contracts:
```
tronbox migrate --network development
```
Run tests:
```
tronbox test test/UserStore.js
```
Run API script:
```
python.exe .\UserStoreAPI.py
```
