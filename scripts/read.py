import json

from web3 import Web3, HTTPProvider

goerli = "https://goerli.infura.io/v3/a11313ddcf61443898b6a47e952d255c"
chiado = "https://rpc.chiadochain.net"

# Connect to your ethereum node
web3 = Web3(HTTPProvider(chiado))

# Contract address
contract_address = '0x09B5065d2924De33C85F76474A89A27189402064'

# Contract ABI
with open('.build/VowelSoundsNFT.json', 'r') as f:
    contract_abi = json.load(f)['abi']

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

breakpoint()

# Call contract function
# data = contract.functions.yourFunctionName().call()
# print(data)
