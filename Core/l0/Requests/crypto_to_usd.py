import requests
import time

def crypto_to_usd(asset = 'ETH'):
    toDo = 0
    while toDo < 3:
        try:
            url = f'https://min-api.cryptocompare.com/data/price?fsym={asset}&tsyms=USDT'
            response = requests.get(url)
            result = [response.json()]
            price = result[0]['USDT']
            return float(price)
        except:
            time.sleep(5)
            toDo = toDo + 1
    # print("\033[31m{}".format('Core -> Instruments -> Balance -> crypto_to_usd(asset) ERROR'))
    # print("\033[0m{}".format(' '))
    # return 'ERROR'
    raise Exception('Getiing Market Data Error')