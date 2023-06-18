import time
from Core.l1.SyncSwapL1 import SyncSwap
from web3 import Web3
from web3 import Account
from Core.l0.Balance.TokenBalance import check_token_balance
from Core.l0.Balance.ZkSyncEthBalance import eth_zk_balance
from Core.l0.Requests.crypto_to_usd import crypto_to_usd
from Core.l0.Tx.TxGg import check_tx_sucs
import random
import json
import tkinter as tk
from Core.l0.Tx.ZkGas import usd_to_zk_gas
Account.enable_unaudited_hdwallet_features()

def to_json(obj):
    obj = str(obj)
    obj = obj.replace('\'', '\"')
    obj = obj.replace('False', 'false')
    obj = obj.replace('True', 'true')
    # moka = json.loads(obj)
    # print(obj)
    return obj


class SyncAccManager:
    state = ''
    file = ''
    acc = ''
    swap = ''
    def __init__(self,file,days=1,okno = 0):
        self.okno = okno
        self.file = file
        self.up_from_json(file)
        self.swaps_manager(days)
    def up_from_json(self,file):

        with open(file) as fileo:
            self.state = json.load(fileo)
        self.file = file
        try:
            self.acc = Account.from_key(self.state['key'])
        except:
            self.acc = Account.from_mnemonic(self.state['key'])
        self.swap = SyncSwap(self.acc,gasForSwap=self.state['modules']['syncSwap']['tx_costs'])

    def up_to_json(self):
        with open(self.file,'w') as fileo:
            fileo.write(to_json(self.state))


    def just_swap(self):
        eth_marker = self.state['modules']['syncSwap']['flags']['eth']

        if eth_marker:
            result = False
            # balance = eth_zk_balance(self.acc.address)

            balance = self.state['modules']['syncSwap']['volume']
            balance = Web3.to_wei(balance/crypto_to_usd(),'ether')
            result = True
            result = self.swap.eth_to_usdc_swap(balance)

            if result:
                self.okno.insert(tk.END, f'\n{self.acc.address} :swaped eth -> usdc ')
                self.state['modules']['syncSwap']['flags']['eth'] =False
                self.up_to_json()
            else:
                self.okno.insert(tk.END, f'\n{self.acc.address} : eth -> usdc error')
                # raise Exception('Error while eth -> usdc')
            # return result

        elif eth_marker == False:
            result = False
            balance = check_token_balance(self.acc.address)
            # balance = float((balance-1)/10**6)
            if self.state['modules']['syncSwap']['flags']['approved'] == False:
                result = True
                result = self.swap.usdc_to_eth_swap(balance)
                if result:
                    self.okno.insert(tk.END, f'\n{self.acc.address} :swaped usdc -> eth ')
                    self.state['modules']['syncSwap']['flags']['approved'] = True
                else:
                    self.okno.insert(tk.END, f'\n{self.acc.address} : usdc -> eth error')
                    # raise Exception('Error while usdc -> eth')

            elif self.state['modules']['syncSwap']['flags']['approved'] == True:
                result = True
                result = self.swap.usdc_to_eth_swap(balance,False)

            if result:
                self.okno.insert(tk.END, f'\n{self.acc.address} :swaped usdc -> eth ')
                self.state['modules']['syncSwap']['flags']['eth'] = True
                self.up_to_json()
            else:
                self.okno.insert(tk.END,f'\n{self.acc.address} : usdc -> eth error')
                # raise Exception('Error while usdc -> eth')

        # if result:
        #     self.state['modules']['syncSwap']['flags']['approved']
        self.up_to_json()
        return result , eth_marker

    def swaps_manager(self,days):
        try:
            time_beetwin = int((days*3600)/((self.state['modules']['syncSwap']['swaps']-self.state['modules']['syncSwap']['flags']['doneTxs'])*2))
        except:
            self.okno.insert(tk.END, f'\n{self.acc.address} акк уже сделан (надо - сделано = 0)\n')
            return
        if self.state['modules']['syncSwap']['flags']['done'] == False:
            for i in range((self.state['modules']['syncSwap']['swaps']-self.state['modules']['syncSwap']['flags']['doneTxs'])*2):
                if self.checker() == False:
                    self.okno.insert(tk.END, f'\n{self.acc.address} Не достаточно средств на газ\n')
                    print('Не достаточно средств на газ')
                    return
                reSwap = self.just_swap()


                if reSwap and self.state['modules']['syncSwap']['flags']['eth'] == True:
                    self.state['modules']['syncSwap']['flags']['doneTxs'] = self.state['modules']['syncSwap']['flags']['doneTxs'] + 1
                    self.up_to_json()
                if self.state['modules']['syncSwap']['flags']['doneTxs']>=self.state['modules']['syncSwap']['swaps']:
                    self.state['modules']['syncSwap']['flags']['done'] = True
                    self.okno.insert(tk.END, f'\n{self.acc.address} Done \n')
                    self.up_to_json()
                slp = time_beetwin+random.randint(-int(time_beetwin/8),int(time_beetwin/8))
                self.okno.insert(tk.END, f'\n{self.acc.address} Sleeping {slp}')
                # print(f'sleeping {slp}')
                time.sleep(slp)
        else:
            self.okno.insert(tk.END, f'\nNo need for {self.acc.address}\n')
            # print(f'\nNo need for {self.acc.address}\n')

    def checker(self):
        volumeusd = self.state['modules']['syncSwap']['volume']
        eth_price = crypto_to_usd('ETH')


        # assets in eth
        if self.state['modules']['syncSwap']['flags']['eth']==True and eth_zk_balance(self.acc.address)-Web3.to_wei(volumeusd/eth_price,'ether') < Web3.to_wei(0.27/eth_price,'ether'):
            return False

        #assets in usdc
        elif self.state['modules']['syncSwap']['flags']['eth']==False and eth_zk_balance(self.acc.address) < Web3.to_wei(0.27/eth_price,'ether'):
            return False

        return True