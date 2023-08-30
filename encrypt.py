import json
from pathlib import Path

import click
from cryptography.fernet import Fernet
from eth_utils import keccak  # type: ignore
from nucypher.blockchain.eth.agents import CoordinatorAgent
from nucypher.blockchain.eth.registry import InMemoryContractRegistry
from nucypher.characters.lawful import Enrico
from nucypher.policy.conditions.lingo import Lingo
from nucypher.utilities.logging import GlobalLoggerSettings
from nucypher_core.ferveo import DkgPublicKey

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
@click.option("--input-dir", type=str, help="Path to the file to be encrypted")
@click.option(
    "--spill-secret-hazmat-hazmat-i-know-what-i-am-doing",
    is_flag=True,
    help="Spill the secret to stdout",
)
@click.option(
    "--ritual-id",
    type=int,
    help="Ritual ID obtained from a side channel",
)
@click.option("--coordinator-provider-uri", type=str, help="URI of the coordinator provider", required=True)
@click.option(
    "--coordinator-network",
    default="mumbai",
    help="Network for the coordinator",
    show_default=True,
    type=click.Choice(["mumbai", "tapir", "polygon", "lynx"]),
)
@click.option("--output-dir", type=str, required=False, help="Output file for encrypted data")
def main(
    input_dir: str,
    ritual_id: int,
    coordinator_provider_uri: str,
    coordinator_network: str,
    output_dir: str,
    spill_secret_hazmat_hazmat_i_know_what_i_am_doing: bool,
):
    if output_dir is None:
        output_dir = input_dir

    # Iterate through the files in input_dir
    dir_path = Path(input_dir)

    file_plaintexts = []

    for file_path in dir_path.iterdir():
        with open(file_path, "rb") as f:
            file_content = f.read()

        file_plaintext = FilePlaintext(file_content=file_content, metadata={"filename": file_path.name})
        file_plaintexts.append(file_plaintext)

    plaintext_of_sym_key = keygen()

    secret_hash = keccak(plaintext_of_sym_key)

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

    is_material_released_condition: Lingo = {
        "version": "1.0.0",
        "condition": {
            "conditionType": "contract",
            "contractAddress": "0x96ebdf35199219BDd16E3c3E1aD8C89C9185b734",  # contract with initialWindow
            "functionAbi": {
                "inputs": [],
                "name": "materialReleaseConditionMet",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },  # type: ignore
            "method": "materialReleaseConditionMet",
            "chain": 5,
            "returnValueTest": {"comparator": "==", "value": True},
        },
    }

    ciphertext_of_sym_key = enrico.encrypt_for_dkg(plaintext=plaintext_of_sym_key, conditions=is_material_released_condition)

    # Encrypt all the files in the directory

    for plaintext in file_plaintexts:
        filename_to_encrypt = plaintext.metadata["filename"]
        print("Encrypting", filename_to_encrypt)
        payload = encapsulate(plaintext_of_sym_key, plaintext.to_bytes())
        tmk = TMK(
            bulk_ciphertext=payload,
            encrypted_sym_key=bytes(ciphertext_of_sym_key),
            conditions=is_material_released_condition,
        )

        # We'll write to the output_path for this filename
        new_filename = filename_to_encrypt + ".encrypted"
        output_filepath = Path(output_dir) / new_filename

        with open(output_filepath, "wb") as file:
            data = tmk.to_bytes()
            file.write(data)
            print(f"Wrote {len(data)} bytes to {output_filepath}")

        ################
        # Sanity check #
        ################

        hopefully_tmk = TMK.from_bytes(data)
        hopefully_cleartext = decrypt(ciphertext=hopefully_tmk.bulk_ciphertext, plaintext_of_symkey=plaintext_of_sym_key)
        hopefully_payload = FilePlaintext.from_bytes(hopefully_cleartext)
        assert hopefully_payload.metadata["filename"] == filename_to_encrypt
        assert hopefully_payload.file_content == plaintext.file_content

    print("Keccak hash of plaintext sym key: ", secret_hash.hex())
    print("Ciphertext of sym key: ", bytes(ciphertext_of_sym_key).hex())

    with open(Path(output_dir) / "encryption_metadata.json", "w") as f:
        encryption_metadata = {
            "ciphertext": bytes(ciphertext_of_sym_key).hex(),
            "secret_hash": secret_hash.hex(),
        }
        f.write(json.dumps(encryption_metadata, indent=4))

    if spill_secret_hazmat_hazmat_i_know_what_i_am_doing:
        print("Here is the sym key:")
        print(plaintext_of_sym_key.hex())
        print("Above is the sym key.")


if __name__ == "__main__":
    main()
