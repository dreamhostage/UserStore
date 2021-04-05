from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
import traceback

contract_address = "TT61YWuH8zdxxHkpntMoBLDny82GzVrvVn"
HTTPprovider = "http://localhost:9090"
userAddress = "THHoZxNjYxMwCvPXWt4dwWjcTN1qTN81go"
userPK = "7cbc531343006ca511b051576053cf48da63c27284db3400ad02eb88633e0b21"

# API class-------------------------------------------------------------------------------------------------------------
class UserStoreAPI(object):

    def __init__(self, HTTPprovider, contract_address):
        self.contract_address = contract_address
        self.HTTPprovider = HTTPprovider
        self.client = Tron(HTTPProvider(HTTPprovider))
        self.contract = self.client.get_contract(contract_address)

    def top_up_address(self, amount, address):
        txn = (
        self.client.trx.transfer("THHoZxNjYxMwCvPXWt4dwWjcTN1qTN81go", address, amount)
        .memo("test memo")
        .fee_limit(100_000_000)
        .build()
        .inspect()
        .sign(PrivateKey(bytes.fromhex('7cbc531343006ca511b051576053cf48da63c27284db3400ad02eb88633e0b21')))
        .broadcast())
        #print(txn)

    def getTokenData(self, key):
        data = self.contract.functions.getTokenData(key)
        if len(data) == 0:
            data = 'Invalid TOKEN'
        return data

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
                print(txn)
                print(receipt)
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

def main():
    input_value = 'q'
    while input_value != '0':
        print ("\n" * 100)
        print(' ------------------------------------')
        print('1 - generate address and private key |')
        print('2 - mint token                       |')
        print('3 - get token data                   |')
        print('4 - get token owner                  |')
        print('5 - transfer token                   |')
        print(' ------------------------------------')
        print('\n')
        print('0 - EXIT')
        print('Select your choice:')
        input_value = input()
        
        if input_value == '1':
            data = contractInstance.client.generate_address()
            contractInstance.top_up_address(15000000, data.get('base58check_address'))
            print ("\n" * 100)
            print('--------------------------------------------------------------------------------------')
            print('| Your address:     ' + data.get('base58check_address') + '                               |')
            print('| Your private key: ' + data.get('private_key') + ' |')
            print('--------------------------------------------------------------------------------------')
            print('Press any key...')
            key = input()
            print ("\n" * 100)
        if input_value == '2':
            print('Enter token data:')
            data = input()
            print('Enter token key:')
            key = input()
            print('Enter your address:')
            address = input()
            print('Enter your Private Key:')
            PK = input()
            mintResponse = contractInstance.mintToken(key, data, address, PK)
            if mintResponse == True:
                print('Mint Token:          OK')
            else:
                print('Mint Token:          Error')
            print('Press any key...')
            input()
        if input_value == '3':
            print ("\n" * 100)
            print('Enter token key:')
            key = input()
            tokenData = contractInstance.getTokenData(key)
            print ("\n" * 100)
            if tokenData == 'Invalid TOKEN':
                print('--------------------------------------------------------------------------------------')
                print('############################## Invalid token key #####################################')
                print('--------------------------------------------------------------------------------------')
            else:
                print('--------------------------------------------------------------------------------------')
                print('Token data:          ' + tokenData)
                print('--------------------------------------------------------------------------------------')
            print('Press any key...')
            input()
        if input_value == '4':
            print ("\n" * 100)
            print('Enter token key:')
            key = input()
            try:
                print ("\n" * 100)
                tokenData = contractInstance.getTokenData(key)
                if tokenData == 'Invalid TOKEN':
                    print('--------------------------------------------------------------------------------------')
                    print('############################## Invalid token key #####################################')
                    print('--------------------------------------------------------------------------------------')
                else:
                    tokenOwner = contractInstance.getTokenOwner(key)
                    print('--------------------------------------------------------------------------------------')
                    print('Token owner:         ' + tokenOwner)
                    print('--------------------------------------------------------------------------------------')
                print('Press any key...')
                input()
            except Exception:
                print('--------------------------------------------------------------------------------------')
                print('############################## Invalid token key #####################################')
                print('--------------------------------------------------------------------------------------')
                print('Press any key...')
                input()
        if input_value == '5':
            print ("\n" * 100)
            print('Enter token key:')
            tKey = input()
            print('Enter transferring address:')
            tAddress = input()
            print('Enter your address:')
            oAddress = input()
            print('Enter your private key:')
            oPK = input()
            response = contractInstance.transferToken(tKey, oAddress, oPK, tAddress)
            if response == True:
                print('Transfering:         OK')
            else:
                print('Transfering:         ERROR')
            print('Press any key...')
            input()


main()

# contractInstance.top_up_address(1000000, 'TJmKM9wSKWALciWYLCYG2enAfekZwgoXDc')
# data = contractInstance.client.get_account_balance('TXuqUTeJQK92fwr4376AJSXoL1nTjCYjBc')
# print(data)