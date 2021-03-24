# UserStore
Install tronbox and npm dependencies:

sudo npm install -g tronbox
docker pull trontools/quickstart
npm install

Now we have to run tron node for development purposes. To run the contrainer use:

docker run -it -p 9090:9090 -v $PWD/accounts-data:/config --rm --name tron trontools/quickstart

Deploy contracts:

tronbox migrate --network development

Run tests:

tronbox test test/UserStore.js

UserStore contract API: UserStoreAPI.py
