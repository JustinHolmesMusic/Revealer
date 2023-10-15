from web3 import Web3

from revealer import deployment_artifacts
from revealer.bob_and_other_networky_things import bob
from revealer.conditions import is_material_released_condition
from nucypher_core import ferveo

def reveal_symmetric_key(contract_address: str):
    w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/08ebc943a2844ce7a78678a320b67d54"))
    abi = deployment_artifacts.abis[1]
    contract = w3.eth.contract(address=contract_address, abi=abi)
    key_ciphertext = contract.functions.keyCiphertext().call()

    ciphertext = ferveo.Ciphertext.from_bytes(key_ciphertext)

    try:
        revealed_sym_key = bob.threshold_decrypt(
            ritual_id=91,  # Cuz 91
            ciphertext=ciphertext,
            conditions=is_material_released_condition,
        )
        return revealed_sym_key
    except bob.NotEnoughNodes as e:
        if "Unauthorized('Decryption conditions not satisfied')" in e.args[0]:
            raise PermissionError("Decryption conditions not satisfied")
        else:
            raise


if __name__ == "__main__":
    reveal_symmetric_key("0xa812137EFf2B368d0B2880A39B609fB60c426850")
