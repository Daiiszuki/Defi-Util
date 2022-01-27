import brownie
from brownie import accounts, network, config
from web3 import Web3
import json 


from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from web3.net import AsyncNet
import os
import asyncio
from json import loads
from decimal import Decimal
from dotenv import load_dotenv 
load_dotenv()
infura_url = "wss://mainnet.infura.io/ws/v3/"
privateKey = os.getenv("PRIVATE_KEY")

web3 = Web3(Web3.WebsocketProvider(infura_url, websocket_timeout=60))

ETHER = 10 ** 18
factoryABI = json.loads('[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

async def get_account():

    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    

async def handle_event(event):
    print(event)
    print(web3.eth.block_number)
    uniswapFactory = '0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95'
    wethAddress = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    daiAddress = '0x2a1530C4C41db0B0b2bB646CB5Eb1A67b7158667'
    
    #print(bid_price, offer_price)
    factory = web3.eth.Contract(factoryABI, uniswapFactory);
    pairAddress = await factory.getPair(wethAddress, daiAddress).call();
    pair = web3.eth.Contract(factory.abi, pairAddress);
    reserves = await pair.getReserves().call();
    print(pairAddress.logs)
    print(reserves.logs)
    print(web3.eth.Eth.get_filter_logs)


    # and whatever

async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            await handle_event(event)
        await asyncio.sleep(poll_interval)

async def main():
    if network.show_active() in ["mainnet-fork"]:
        await get_account()
    block_filter = web3.eth.filter('latest')
    #tx_filter = web3.eth.filter('pending')
    wethAddress = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    daiAddress = '0x2a1530C4C41db0B0b2bB646CB5Eb1A67b7158667'
    uniswapFactory = '0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95'
    factory = web3.eth.Contract(factoryABI, uniswapFactory);
    pairAddress = await factory.getPair(wethAddress, daiAddress).call();
    event_filter = web3.eth.filter({"address": pairAddress })
    loop = asyncio.get_event_loop()


    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(block_filter, 2),
                log_loop(event_filter, 2)
                ))
    finally:
        loop.close()

if __name__ == '__main__':
    asyncio.run(main())


 


