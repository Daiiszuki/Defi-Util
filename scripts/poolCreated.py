from web3 import Web3
from .utils import create_contract
from .events import fetch_events
import json
from json import loads

from brownie import accounts, network, config

from dotenv import load_dotenv 
import os
from web3._utils.contracts import encode_abi
#from web3._utils.contracts import encode_abi




load_dotenv()
prjectId = os.getenv("WEB3_INFURA_PROJECT_ID")
infura_url = 'https://mainnet.infura.io/v3/' + prjectId

web3 = Web3(Web3.HTTPProvider(infura_url))
    
#https://ethereum.stackexchange.com/questions/51637/get-all-the-past-events-of-the-contract

#uniswap_factory = '0x1F98431c8aD98523631AE4a59f267346ea31F984'
#factory_abi_url = 'https://unpkg.com/@uniswap/v2-core@1.0.1/build/UniswapV2Factory.json'
#erc20ABI = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')

erc20ABI = 'https://unpkg.com/@uniswap/v2-core@1.0.1/build/IERC20.json'

def fetch_uniswap_pairs():
    """Fetch all trading pairs on Uniswap"""
    
    factoryAddress =  Web3.toChecksumAddress('0x1F98431c8aD98523631AE4a59f267346ea31F984')
    factoryAbi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint24","name":"fee","type":"uint24"},{"indexed":true,"internalType":"int24","name":"tickSpacing","type":"int24"}],"name":"FeeAmountEnabled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnerChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":true,"internalType":"uint24","name":"fee","type":"uint24"},{"indexed":false,"internalType":"int24","name":"tickSpacing","type":"int24"},{"indexed":false,"internalType":"address","name":"pool","type":"address"}],"name":"PoolCreated","type":"event"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"}],"name":"createPool","outputs":[{"internalType":"address","name":"pool","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickSpacing","type":"int24"}],"name":"enableFeeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint24","name":"","type":"uint24"}],"name":"feeAmountTickSpacing","outputs":[{"internalType":"int24","name":"","type":"int24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint24","name":"","type":"uint24"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"parameters","outputs":[{"internalType":"address","name":"factory","type":"address"},{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickSpacing","type":"int24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"setOwner","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
    
    factory = web3.eth.contract(address=factoryAddress,abi=factoryAbi)
    events = list(fetch_events(factory.events.PoolCreated, from_block=0, to_block='latest'))


    
    print('Got', len(events), 'events')

    # Each event.args is presented as AttrbuteDict
    # AttributeDict({'args': AttributeDict({'token0': '0x607F4C5BB672230e8672085532f7e901544a7375', 'token1': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'pair': '0x6d57a53A45343187905aaD6AD8eD532D105697c1', '': 94}), 'event': 'PairCreated', 'logIndex': 7, 'transactionIndex': 2, 'transactionHash': HexBytes('0xa0ce4b0db9bbf7887f09c4b35ec1167144b06f69fbbea6d6a163a72db28175d8'), 'address': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f', 'blockHash': HexBytes('0xf269a89cf729781bfa8e8ec421f8eefbf13e1fecd22b4118c1304d360832ef20'), 'blockNumber': 10092190})
    count = 0 
    for ev in events[0:10]:
      count += 1

      token0 = create_contract(web3, erc20ABI, ev.args.token0)
      token1 = create_contract(web3, erc20ABI, ev.args.token1)
      #try:
      print(f'Found pair {count} {token0.functions.name().call()}-{token1.functions.name().call()}')
      print(str(ev.args))
      print("====================================\n\n\n\n\n\n\n")
      #except OverflowError:
      print("An exception has occured")

def main():
    fetch_uniswap_pairs()



