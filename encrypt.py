import argparse
import base64
import json
from pathlib import Path

from cryptography.fernet import Fernet
from eth_utils import keccak  # type: ignore
from nucypher.blockchain.eth.agents import CoordinatorAgent
from nucypher.blockchain.eth.registry import InMemoryContractRegistry
from nucypher.characters.lawful import Enrico
from nucypher.policy.conditions.lingo import ConditionLingo, Lingo
from nucypher.utilities.logging import GlobalLoggerSettings
from nucypher_core.ferveo import DkgPublicKey

from revealer_bot.types import TMK

######################
# Boring setup stuff #
######################

LOG_LEVEL = "info"
GlobalLoggerSettings.set_log_level(log_level_name=LOG_LEVEL)
GlobalLoggerSettings.start_console_logging()

#####################
# Scully the Symmet
#####################


def keygen() -> bytes:
    _secret = Fernet.generate_key()
    return _secret


def encapsulate(secret: bytes, clear_text: bytes) -> bytes:
    f = Fernet(secret)
    capsule = f.encrypt(clear_text)
    return capsule


def main(args):
    file_path = Path(args.file_path)

    with open(file_path, "rb") as f:
        clear_text = f.read()

    plaintext_of_sym_key = keygen()

    secret_hash = keccak(plaintext_of_sym_key)
    bulk_ciphertext = encapsulate(plaintext_of_sym_key, clear_text)

    print("--------- Threshold Encryption ---------")

    coordinator_agent = CoordinatorAgent(
        provider_uri=args.coordinator_provider_uri,
        registry=InMemoryContractRegistry.from_latest_publication(
            network=args.coordinator_network
        ),
    )
    ritual_id = args.ritual_id
    ritual = coordinator_agent.get_ritual(ritual_id)
    enrico = Enrico(encrypting_key=DkgPublicKey.from_bytes(bytes(ritual.public_key)))

    print(
        f"Fetched DKG public key {bytes(enrico.policy_pubkey).hex()} "  # type: ignore
        f"for ritual #{ritual_id} "
        f"from Coordinator {coordinator_agent.contract.address}"
    )

    eth_balance_condition: Lingo = {
        "version": ConditionLingo.VERSION,
        "condition": {
            "chain": args.chain,
            "method": "eth_getBalance",
            "parameters": [args.eth_address, "latest"],
            "returnValueTest": {"comparator": "==", "value": 0},
        },
    }

    ciphertext_of_sym_key = enrico.encrypt_for_dkg(
        plaintext=plaintext_of_sym_key, conditions=eth_balance_condition
    )

    tmk: TMK = {
        "bulk_ciphertext": base64.b64encode(bytes(bulk_ciphertext)).decode(),  # Encrypted Tony
        "encrypted_sym_key": bytes(ciphertext_of_sym_key).hex(),
        "conditions": eth_balance_condition,
        "filename": file_path.name,
    }

    ################
    # Sanity check #
    ################

    f = Fernet(plaintext_of_sym_key)
    hopefully_decrypted = f.decrypt(bulk_ciphertext)
    assert hopefully_decrypted == clear_text

    ##################

    tmk_json = json.dumps(tmk)

    filename = args.output_file
    with open(filename, "w") as file:
        data = tmk_json
        file.write(data)
        print(f"Wrote {len(data)} bytes to {filename}")

    print("Keccak hash of plaintext sym key: ", secret_hash.hex())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt file using threshold encryption.")
    parser.add_argument(
        "--file_path", type=str, default="manzana.mp3", help="Path to the file to be encrypted"
    )
    parser.add_argument(
        "--ritual_id", type=int, help="Ritual ID obtained from a side channel", default=15
    )
    parser.add_argument(
        "--coordinator_provider_uri",
        type=str,
        help="URI of the coordinator provider",
        required=True,
    )
    parser.add_argument(
        "--coordinator_network",
        type=str,
        default="mumbai",
        help="Network for the coordinator",
        choices=["mumbai", "rinkeby", "mainnet", "goerli", "ropsten", "kovan"],
    )
    parser.add_argument("--chain", type=int, help="Ethereum chain ID", default=80001)
    parser.add_argument(
        "--eth_address",
        type=str,
        help="Ethereum address for balance check",
        default="0x210eeAC07542F815ebB6FD6689637D8cA2689392",
    )
    parser.add_argument(
        "--output-file", type=str, default="tony.tmk", help="Output file for encrypted data"
    )

    args = parser.parse_args()
    main(args)
