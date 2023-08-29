import click
from cryptography.fernet import Fernet
from eth_utils import keccak  # type: ignore
from nucypher_core.ferveo import DkgPublicKey
from pathlib import Path

from nucypher.blockchain.eth.agents import CoordinatorAgent
from nucypher.blockchain.eth.registry import InMemoryContractRegistry
from nucypher.characters.lawful import Enrico
from nucypher.policy.conditions.lingo import ConditionLingo, Lingo
from nucypher.utilities.logging import GlobalLoggerSettings
from revealer_bot.tmk import TMK, FilePlaintext, decrypt, encapsulate

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


@click.command()
@click.option(
    "--input-dir", type=str, help="Path to the file to be encrypted"
)
@click.option(
    "--spill-secret-hazmat-hazmat-i-know-what-i-am-doing", is_flag=True, help="Spill the secret to stdout",
)
@click.option(
    "--ritual-id",
    type=int,
    help="Ritual ID obtained from a side channel",
)
@click.option(
    "--coordinator-provider-uri", type=str, help="URI of the coordinator provider", required=True
)
@click.option(
    "--coordinator-network",
    default="mumbai",
    help="Network for the coordinator",
    show_default=True,
    type=click.Choice(["mumbai", "rinkeby", "mainnet", "goerli", "ropsten", "kovan"]),
)
@click.option("--chain", type=int, help="Ethereum chain ID", default=80001, show_default=True)
@click.option(
    "--eth-address",
    type=str,
    help="Ethereum address for balance check",
    default="0x210eeAC07542F815ebB6FD6689637D8cA2689392",
    show_default=True,
)
@click.option(
    "--eth-minimum-balance",
    type=float,
    help="Ethereum minimum balance condition",
    default=0,
    show_default=True,
)
@click.option("--output-file", type=str, default="tony.tmk", help="Output file for encrypted data")
def main(
    input_file: str,
    ritual_id: int,
    coordinator_provider_uri: str,
    coordinator_network: str,
    chain: int,
    eth_address: str,
    eth_minimum_balance: float,
    output_file: str,
):
    file_path = Path(input_file)

    with open(file_path, "rb") as f:
        file_content = f.read()

    payload = Payload(file_content=file_content, metadata={"filename": file_path.name})

    plaintext_of_sym_key = keygen()
    secret_hash = keccak(plaintext_of_sym_key)
    bulk_ciphertext = encapsulate(plaintext_of_sym_key, payload.to_bytes())

    print("--------- Threshold Encryption ---------")

    coordinator_agent = CoordinatorAgent(
        provider_uri=coordinator_provider_uri,
        registry=InMemoryContractRegistry.from_latest_publication(network=coordinator_network),
    )
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
            "chain": chain,
            "method": "eth_getBalance",
            "parameters": [eth_address, "latest"],
            "returnValueTest": {"comparator": ">=", "value": eth_minimum_balance},
        },
    }

    ciphertext_of_sym_key = enrico.encrypt_for_dkg(
        plaintext=plaintext_of_sym_key, conditions=eth_balance_condition
    )

    tmk = TMK(
        bulk_ciphertext=bulk_ciphertext,
        encrypted_sym_key=bytes(ciphertext_of_sym_key),
        conditions=eth_balance_condition,
    )

    with open(output_file, "wb") as file:
        data = tmk.to_bytes()
        file.write(data)
        print(f"Wrote {len(data)} bytes to {output_file}")

    print("Keccak hash of plaintext sym key: ", secret_hash.hex())
    ################
    # Sanity check #
    ################

    hopefully_tmk = TMK.from_bytes(data)
    hopefully_cleartext = decrypt(
        ciphertext=hopefully_tmk.bulk_ciphertext, plaintext_of_symkey=plaintext_of_sym_key
    )
    hopefully_payload = Payload.from_bytes(hopefully_cleartext)
    assert hopefully_payload.metadata["filename"] == payload.metadata["filename"]
    assert hopefully_payload.file_content == payload.file_content


if __name__ == "__main__":
    main()
