import base64
import json

from nucypher_core.ferveo import DkgPublicKey

from nucypher.blockchain.eth.agents import CoordinatorAgent
from nucypher.blockchain.eth.registry import InMemoryContractRegistry
from nucypher.characters.lawful import Enrico
from nucypher.policy.conditions.lingo import ConditionLingo
from nucypher.utilities.logging import GlobalLoggerSettings

######################
# Boring setup stuff #
######################

LOG_LEVEL = "info"
GlobalLoggerSettings.set_log_level(log_level_name=LOG_LEVEL)
GlobalLoggerSettings.start_console_logging()

staking_provider_uri = 
network = "lynx"

coordinator_provider_uri = 
coordinator_network = "mumbai"

#####################
# Scully the Symmet
#####################
from cryptography.fernet import Fernet
from eth_utils import keccak

def keygen():
    _secret = Fernet.generate_key()
    return _secret

with open('manzana.mp3', 'rb') as tony:
    definitely_tony = tony.read()

def encapsulate(secret):
    f = Fernet(secret)
    capsule = f.encrypt(definitely_tony)
    return capsule

plaintext_of_sym_key = keygen()
secret_hash = keccak(plaintext_of_sym_key)
bulk_ciphertext = encapsulate(plaintext_of_sym_key)

print(f"secret: {plaintext_of_sym_key.hex()}")
print(f"secret hash: {secret_hash.hex()}")
print(f"secret ciphertext: {bulk_ciphertext.hex()}")

###############
# Enrico
###############

print("--------- Threshold Encryption ---------")

coordinator_agent = CoordinatorAgent(
    provider_uri=coordinator_provider_uri,
    registry=InMemoryContractRegistry.from_latest_publication(
        network=coordinator_network
    ),
)
ritual_id = 15  # got this from a side channel
ritual = coordinator_agent.get_ritual(ritual_id)
enrico = Enrico(encrypting_key=DkgPublicKey.from_bytes(bytes(ritual.public_key)))

print(
    f"Fetched DKG public key {bytes(enrico.policy_pubkey).hex()} "
    f"for ritual #{ritual_id} "
    f"from Coordinator {coordinator_agent.contract.address}"
)

eth_balance_condition = {
    "version": ConditionLingo.VERSION,
    "condition": {
        "chain": 80001,
        "method": "eth_getBalance",
        "parameters": ["0x210eeAC07542F815ebB6FD6689637D8cA2689392", "latest"],
        "returnValueTest": {"comparator": "==", "value": 0},
    },
}

message = "hello world".encode()
ciphertext = enrico.encrypt_for_dkg(plaintext=message, conditions=eth_balance_condition)

print(f"Encrypted message: {bytes(ciphertext).hex()}")
   
tmk = {
    'ciphertext': base64.b64encode(bytes(ciphertext)).decode(),
    'conditions': eth_balance_condition
}

tmk_json = json.dumps(tmk)

filename = 'example.tmk'
with open(filename, 'w') as file:
    data = tmk_json
    file.write(data)
    print(f'Wrote {len(data)} bytes to {filename}')
