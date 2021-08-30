#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime


wallet = ' ' #Insert your wallet address
ifttt_key = ' ' #Insert your IFTTT key

def get_balance():
    request_acc_balance = requests.get('https://api.helium.io/v1/accounts/' + wallet)
    acc_balance_json = json.loads(request_acc_balance.text)
    balance = round((acc_balance_json['data']['balance'])/100000000,2)
    return(balance)

print('Running...')

while 1 == 1:
    previous_balance = get_balance()
    time.sleep(1800)
    current_balance = get_balance()

    if previous_balance < current_balance:      
        
        request_hnt_price = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=helium&vs_currencies=EUR")
        hnt_price_json = json.loads(request_hnt_price.text)
        price = round(hnt_price_json['helium']['eur'],2)
        
        wallet_balance = round(price * current_balance,2)
        
        data = {"value1":str(wallet_balance)}

        r = requests.post('https://maker.ifttt.com/trigger/reward_recieved/with/key/' + ifttt_key, data)
        
        print('Your wallet is now worth: ' + str(wallet_balance) + '€ ' + str(datetime.now()))

        f = open("log.txt", "a")
        f.write('Your wallet is now worth: ' + str(wallet_balance) + '€ ' + str(datetime.now()))
        f.write('\n')
        f.close()
