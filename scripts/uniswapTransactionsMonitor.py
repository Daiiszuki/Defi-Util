from web3 import Web3
import asyncio

import brownie
from brownie import accounts, network, config
#from web3.auto import w3
import json 
import time 

from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from web3.net import AsyncNet
import os
#import asyncio
from json import loads
from decimal import Decimal
from dotenv import load_dotenv 
load_dotenv()
infura_url = "wss://mainnet.infura.io/ws/v3/4ef10d02317e459f82301f76926af721"
privateKey = os.getenv("PRIVATE_KEY")

web3 = Web3(Web3.WebsocketProvider(infura_url, websocket_timeout=60))
async def handle_event(event):
    ts = time.time()
    print('===== BLOCK HASH:  ', event.hex())
    block_hash = event.hex()
    block = web3.eth.getBlock(block_hash, full_transactions=True)
    transactions = block['transactions']
    print('===== BLOCK NUMBER: ', block['number'])
    for tx in transactions:
        print(ts, '   FROM: ', tx['from'])
        print(ts, '   Value ETH: ', web3.fromWei(tx['value'],'ether'))
    print('=======================================\n\n')
    
    
    

    # and whatever

async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            await handle_event(event)
                
        await asyncio.sleep(poll_interval)

def main():
    block_filter = web3.eth.filter('latest')
    
    #tx_filter = web3.eth.filter('latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(block_filter, 2)
                #,
                #log_loop(tx_filter, 2)
                ))
    finally:
        loop.close()

if __name__ == '__main__':
    main()