import json
from web3 import Account
from web3 import Web3
# from Core.Settings.Paths import syncPathSettings
syncPathSettings = 'Accs/settings.json'

def to_json(obj):
    obj = str(obj)
    obj = obj.replace('\'', '\"')
    obj = obj.replace('False', 'false')
    obj = obj.replace('True', 'true')
    # moka = json.loads(obj)
    # print(obj)
    return obj


class setJsonAcc:
    eralendData = ''
    reactorData = ''
    spaceData = ''
    domains = ''
    sync = ''

    def __init__(self):
        Account.enable_unaudited_hdwallet_features()
    # def syncSwap(self,swaps,vol):
    #     self.sync = {"swaps": swaps, "volume": vol}
    def syncSwap(self):
        with open(syncPathSettings) as file:
            self.sync = json.load(file)
            self.sync['flags'] = {'done': False, 'doneTxs': 0, 'mistakes': 0,'eth':True,'approved':False}

    def eralend(self, vol:float, borrow=0.71):
        data = {'volume': vol, 'borrow': borrow, 'flags': {'done': False, 'borrowed': False, 'mistakes': 0}}
        # self.eralendData = to_json(data)
        self.eralendData = data

    def reactor(self, vol:float, borrow=0.68):
        data = {'volume': vol, 'borrow': borrow, 'flags': {'done': False, 'borrowed': False, 'mistakes': 0}}
        # self.reactorData = to_json(data)
        self.reactorData = data

    def space(self, vol:float, amount:int):
        data = {'volume': vol, 'txs': amount, 'flags': {'done': False, 'doneTxs': 0, 'mistakes': 0}}
        # self.spaceData = to_json(data)
        self.spaceData = data

    def mintDomain(self, namelist:str):
        data = {'nameList': namelist}
        self.domains = data

    def setInfo(self, mnemonic_or_key):
        Account.enable_unaudited_hdwallet_features()
        try:
            try:
                acc = Account.from_key(mnemonic_or_key)
            except:
                acc = Account.from_mnemonic(mnemonic_or_key)

            data = to_json({'address': str(Web3.to_checksum_address(acc.address)), 'key': mnemonic_or_key, 'domain': '',
                            'modules': {'eralend': self.eralendData, 'reactor': self.reactorData, 'space': self.spaceData,
                                        'domains': self.domains, 'syncSwap':self.sync}})
            # print(data)
            return data
        except:
            return 'ERROR'

        # self.address = Web3.to_checksum_address(acc.address)
        # self.key = acc.key