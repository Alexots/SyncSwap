from web3 import Web3
import json
import time


def check_token_balance(address, rpc='https://mainnet.era.zksync.io', token_address='0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4', ABI = None):
    toDo = 0
    while toDo<3:
        try:
            if ABI == None:

                with open('Core/Data/erc20abi.json') as jsonabi:
                    ABI = json.load(jsonabi)
                    # print(ABI)

            if True:
                web3 = Web3(Web3.HTTPProvider(rpc))
                token = web3.eth.contract(address=web3.to_checksum_address(token_address), abi=ABI)
                token_balance = token.functions.balanceOf(web3.to_checksum_address(address)).call()
                return token_balance

        except:
            time.sleep(5)
            toDo = toDo + 1
    raise Exception('ERC20 Token Balance Error')