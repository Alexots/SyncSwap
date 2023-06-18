from Core.l0.Balance.ZkSyncEthBalance import eth_zk_balance
from Core.l0.Requests.crypto_to_usd import crypto_to_usd
from Core.l0.Balance.TokenBalance import check_token_balance
from web3 import Web3

def check_if_ready(address,volume_to_swap,tx_costs,tx_how_many):
    balance = float(Web3.from_wei(eth_zk_balance(address),'ether'))*crypto_to_usd()

    balance = balance - volume_to_swap
    txs = (balance/tx_costs)/2

    if balance<0:
        return (False,0)
    if tx_how_many>txs:
        return (False,txs)
    if tx_how_many<=txs:
        return (True,txs)

# print(check_if_ready('0x8f47fbF8A925261c5dd2de89Ede28c39eE47996B',3,0.24,7))

