from web3 import Web3
import time

def check_tx_sucs(tx,rpc="https://mainnet.era.zksync.io"):
    toDo = 0
    while toDo<3:
        try:
            w3 = Web3(Web3.HTTPProvider(rpc))
            txn = w3.eth.get_transaction_receipt(tx)
            status = txn['status']
            if status == 1:
                return True
            else:
                return False
        except:
            time.sleep(3)
            toDo = toDo + 1
    # print("\033[31m{}".format('Core -> Utils -> Tx -> check_tx_sucs(tx,rpc) ERROR'))
    # print("\033[37m{}".format(' '))
    raise Exception('Checking tx sucs Error')