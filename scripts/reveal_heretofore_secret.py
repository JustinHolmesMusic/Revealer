from web3 import Web3
from revealer import deployment_artifacts
def main():
    contract_address = "0xa812137EFf2B368d0B2880A39B609fB60c426850"
    # Get ciphertext from contract

    w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/adc98e27c31d4eca8ed8e4e7f7d35b8f"))
    abi = deployment_artifacts.abis[1]
    contract = w3.eth.contract(address=contract_address, abi=abi)

    key_ciphertext = contract.functions.keyCiphertext().call()

    ciphertext = contract.keyCiphertext()

    bob.threshold_decrypt(
        ritual_id=91,  # Cuz 91
        ciphertext=ciphertext_to_decrypt_with_threshold,
        conditions=tmk.conditions,
    )


if __name__ == "__main__":
    main()
