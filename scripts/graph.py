from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
sample_transport=RequestsHTTPTransport(
   url='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2',
   verify=True,
   retries=5,
)
client = Client(
   transport=sample_transport
)

# Get the value of SNX/ETH 
query = gql('''
query {
 pair(id: "0x157Dfa656Fdf0D18E1bA94075a53600D81cB3a97"){
     reserve0
     reserve1
}
}
''')
response = client.execute(query)
snx_eth_pair = response['pair']
eth_value = float(snx_eth_pair['reserve1']) / float(snx_eth_pair['reserve0'])

# Get the value of ETH/DAI
query = gql('''
query {
 pair(id: "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11"){
     reserve0
     reserve1
}
}
''')
response = client.execute(query)
eth_dai_pair = response['pair']
dai_value = float(eth_dai_pair['reserve0']) / float(eth_dai_pair['reserve1'])

snx_dai_value = eth_value * dai_value

def main():
    print("\n\n=========================================================")
    print("The current price of UMA is: " + str(snx_dai_value) +" DAI")
    print("=============================================================\n\n")
