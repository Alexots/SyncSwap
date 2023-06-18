# from zksync2.module.module_builder import ZkSyncBuilder
# from zksync2.core.types import EthBlockParams
from web3 import Web3
import time

def eth_zk_balance(address):
    address = Web3.to_checksum_address(address)
    toDo = 0

    while toDo < 3:
        try:
            w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
            balance = w3.eth.get_balance(address)
            return balance
        except:
            toDo = toDo + 1
            time.sleep(5)
        # try:
        #     ZKSYNC_PROVIDER = "https://mainnet.era.zksync.io"
        #     zksync_web3 = ZkSyncBuilder.build(ZKSYNC_PROVIDER)
        #     zk_balance = zksync_web3.zksync.get_balance(address, EthBlockParams.LATEST.value)
        #     return zk_balance
        # except:
        #
        #     toDo = toDo + 1
        #     time.sleep(5)
    # print("\033[31m{}".format('Core -> Utils -> Balance -> eth_zk_balance(address) ERROR'))
    # print("\033[0m{}".format(' '))
    # return 'ERROR'
    raise Exception('ZkSync Eth Balance Error')
    # print(f"Balance: {zk_balance}")