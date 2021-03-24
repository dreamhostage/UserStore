from tprpy import Tpr
from tprpy.keys import PrivateKey
from tprpy.providers import HTTPProvider
import traceback

contract_address = "TV89ZUZvaeUnWDiA7LUpds9HewUpmCVtmC"
HTTPprovider = "http://localhost:9090"
userAddress = "THHoZxNjYxMwCvPXWt4dwWjcTN1qTN81go"
userPK = "7cbc531343006ca511b051576053cf48da63c27284db3400ad02eb88633e0b21"

# API class-------------------------------------------------------------------------------------------------------------
class UserStoreAPI(object):

    def __init__(self, HTTPprovider, contract_address):
        self.contract_address = contract_address
        self.HTTPprovider = HTTPprovider
        self.client = Tpr(HTTPProvider(HTTPprovider))
        self.contract = self.client.get_contract(contract_address)

    def getTokenData(self, key):
        return self.contract.functions.getTokenData(key)

    def getTokenOwner(self, key):
        return self.contract.functions.getTokenOwner(key)

    def mintToken(self, key, data, address, PK):
        try:
            txn = (self.contract.functions.mintToken(key, data)
            .with_owner(address)
            .fee_limit(1_000_000000)
            .build()
            .sign(PrivateKey(bytes.fromhex(PK)))
            .broadcast())
            receipt = txn.wait()
            if receipt.get('receipt').get('result') == 'SUCCESS':
                return True
            else:
                return 'REVERT'
        except Exception as e:
            return e

    def transferToken(self, key, fromAddress, fromPK, toAddress):
        try:
            txn = (self.contract.functions.transferToken(key, toAddress)
            .with_owner(fromAddress)
            .fee_limit(1_000_000000)
            .build()
            .sign(PrivateKey(bytes.fromhex(fromPK)))
            .broadcast())
            receipt = txn.wait()
            if receipt.get('receipt').get('result') == 'SUCCESS':
                return True
            else:
                return 'REVERT'
        except Exception as e:
            return e

    def changeTokenData(self, key, data, ownerAddress, ownerPK):
        try:
            txn = (self.contract.functions.changeTokenData(key, data)
            .with_owner(ownerAddress)
            .fee_limit(1_000_000000)
            .build()
            .sign(PrivateKey(bytes.fromhex(ownerPK)))
            .broadcast())
            receipt = txn.wait()
            if receipt.get('receipt').get('result') == 'SUCCESS':
                return True
            else:
                return 'REVERT'
        except Exception as e:
            return e
# Tests-------------------------------------------------------------------------------------------------------------

contractInstance = UserStoreAPI(HTTPprovider, contract_address)
tokenKey = 'Token key'
tokenData = '1'
NewTokenData = '2'
transferAddress = 'TCkkvpLD1v8Cn6m412GHS2gZN2fqUT7vVV'
transferAddressPK = 'ef84a04038a9b34ebc353daaa57abe99b4c6b6235631ccf7cc1baeb7fc41c39a'

response = contractInstance.mintToken(tokenKey, tokenData, userAddress, userPK)

if response == True:
    print('Mint Token:          OK')
else:
    print(response)

tokenData = contractInstance.getTokenData(tokenKey)
print('Token data:          ' + tokenData)

tokenOwner = contractInstance.getTokenOwner(tokenKey)
print('Token owner:         ' + tokenOwner)

response = contractInstance.transferToken(tokenKey, userAddress, userPK, transferAddress)

if response == True:
    print('Transfering:         OK')
else:
    print(response)

NewTokenOwner = contractInstance.getTokenOwner(tokenKey)
print('New token owner:     ' + NewTokenOwner)

if contractInstance.changeTokenData(tokenKey, NewTokenData, transferAddress, transferAddressPK) == True:
    print('Changing Token data: OK')
else:
    print('Changing Token data: ERROR')

tokenData = contractInstance.getTokenData(tokenKey)
print('New token data:      ' + tokenData)
