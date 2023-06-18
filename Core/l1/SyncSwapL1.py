
from web3 import Web3
from web3 import Account
import json
import time

# from Core.Settings.Gas import GasForUsdcZkApprove, GasForSwap
# from Core.Settings.Paths import syncSwapAbi
# from Core.Settings.Paths import erc20abi
# from Core.Settings.Tx import minReceive

from Core.l0.Balance.TokenBalance import check_token_balance
from Core.l0.Balance.ZkSyncEthBalance import eth_zk_balance
from Core.l0.Tx.TxGg import check_tx_sucs
from Core.l0.Requests.crypto_to_usd import crypto_to_usd
from Core.l0.Tx.ZkGas import usd_to_zk_gas

erc20abi = 'Core/Data/erc20abi.json'
syncSwapAbi = 'Core/Data/syncSwapAbi.json'




class SyncSwap:
    abi = ''
    contract_usdc = '0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4'
    swap_contract = '0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295'
    acc = ''

    def __init__(self,acc,gasForApprove = 0.25,gasForSwap=0.3,mink=0.92):
        self.load_abi()
        self.initWeb3()
        self.acc = acc
        self.gasForApprove = usd_to_zk_gas(gasForApprove)
        self.gasForSwap = usd_to_zk_gas(gasForSwap)
        self.mink = mink


    def initWeb3(self):
        self.w3 = Web3(Web3.HTTPProvider("https://mainnet.era.zksync.io"))

    def load_abi(self):
        try:
            with open(syncSwapAbi) as fileJson:
                self.abi = json.load(fileJson)
        except:
            print('SyncSwap load abi Error')
            return 'ERROR'

    def prepare_bytes_for_sync_eth_to_usdc(self,address):

        addressb = bytes.fromhex(address[2:])
        s = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Z\xeaWu\x95\x9f\xbc%W\xcc\x87\x89\xbc\x1b\xf9\n#\x9d\x9a\x91\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        e = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
        con = s + addressb + e
        return con

    def prepare_bytes_for_sync_usdc_to_eth(self,address):

        addressb = bytes.fromhex(address[2:])
        s = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x003U\xdfmL\x9c05rO\xd0\xe3\x91M\xe9jZ\x83\xaa\xf4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        e = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
        con = s + addressb + e
        return con

    def approve_zk_usdc(self,acc, address):
        try:
            Aprove_abi = ''
            with open(erc20abi) as file:
                Aprove_abi = json.load(file)
            w3 = Web3(Web3.HTTPProvider("https://mainnet.era.zksync.io"))
            contract_approve = w3.eth.contract('0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4', abi=Aprove_abi)
            approve_args = [Web3.to_checksum_address(address),2**256-1]
            # check_token_balance(Web3.to_checksum_address(acc.address), "https://mainnet.era.zksync.io",
            #                                                 '0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4')
            approve_txn = contract_approve.functions.approve(*approve_args)
            builded_approve = approve_txn.build_transaction({
                'chainId': 324,
                'from': Web3.to_checksum_address(acc.address),
                'value': Web3.to_wei(0,'ether'),
                'gas': self.gasForApprove,
                'nonce': w3.eth.get_transaction_count(acc.address),
                'maxFeePerGas': 250000000,
                'maxPriorityFeePerGas': 250000000
            })
            signed_approve = w3.eth.account.sign_transaction(builded_approve, acc.key)
            txn_hash_approve = w3.eth.send_raw_transaction(signed_approve.rawTransaction)
            txn_approve_text = txn_hash_approve.hex()
            return txn_approve_text
        except:
            print("\033[31m{}".format('Core -> Utils -> Balance -> approve_zk_usdc(asset) ERROR'))
            print("\033[0m{}".format(' '))
            return 'ERROR'

    def eth_to_usdc_swap(self,ammount_in_eth_wei):
        time.sleep(1)
        value = ammount_in_eth_wei
        valueReceive = int((self.mink*(crypto_to_usd()*ammount_in_eth_wei))/10**12)
        nonce = self.w3.eth.get_transaction_count(self.acc.address)
        contract = self.w3.eth.contract(self.swap_contract,abi=self.abi)

        dead_line = int(time.time() + 3600 * 3)
        args = [[([('0x80115c708E12eDd42E504c1cD52Aea96C547c05c', self.prepare_bytes_for_sync_eth_to_usdc(self.acc.address),
                    '0x0000000000000000000000000000000000000000',
                    b'')],
                  '0x0000000000000000000000000000000000000000',
                  value)],
                valueReceive,
                dead_line]

        txn = contract.functions.swap(*args)
        builded_txn = txn.build_transaction({
            'chainId': 324,
            'from': Web3.to_checksum_address(self.acc.address),
            'value': value,
            'gas': self.gasForSwap,
            'nonce': nonce,
            'maxFeePerGas': 250000000,
            'maxPriorityFeePerGas': 250000000
        })

        signed_txn = self.w3.eth.account.sign_transaction(builded_txn, self.acc.key)
        txn_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_text = txn_hash.hex()

        time.sleep(10)
        return check_tx_sucs(txn_text)

    def usdc_to_eth_swap(self,ammount_in_usdc_wei,needApprove = True):
        value = ammount_in_usdc_wei
        time.sleep(1)
        valueReceive = int(self.mink*(ammount_in_usdc_wei/crypto_to_usd())*10**12)
        # nonce = self.w3.eth.get_transaction_count(self.acc.address)
        contract = self.w3.eth.contract(self.swap_contract,abi=self.abi)

        dead_line = int(time.time() + 3600 * 3)
        args = [[([('0x80115c708E12eDd42E504c1cD52Aea96C547c05c', self.prepare_bytes_for_sync_usdc_to_eth(self.acc.address),
                    '0x0000000000000000000000000000000000000000',
                    b'')],
                  '0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4',
                  value)],
                valueReceive,
                dead_line]
        txn = contract.functions.swap(*args)


        if needApprove:
            print(self.approve_zk_usdc(self.acc,self.swap_contract))
            time.sleep(60)

        builded_txn = txn.build_transaction({
            'chainId': 324,
            'from': Web3.to_checksum_address(self.acc.address),
            'value': Web3.to_wei(0,'ether'),
            'gas': self.gasForSwap,
            'nonce': self.w3.eth.get_transaction_count(self.acc.address),
            'maxFeePerGas': 250000000,
            'maxPriorityFeePerGas': 250000000
        })

        signed_txn = self.w3.eth.account.sign_transaction(builded_txn, self.acc.key)
        txn_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_text = txn_hash.hex()

        time.sleep(10)
        return check_tx_sucs(txn_text)



