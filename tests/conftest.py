import pytest
import json
from nucypher.characters.chaotic import NiceGuyEddie as _Enrico
from nucypher.characters.chaotic import ThisBobAlwaysDecrypts as _Bob
from nucypher.policy.conditions.lingo import ConditionLingo
from nucypher.policy.conditions.evm import _CONDITION_CHAINS


@pytest.fixture
def owner(accounts):
    return accounts[0]

@pytest.fixture
def receiver(accounts):
    return accounts[1]

@pytest.fixture
def not_owner(accounts):
    return accounts[2]

@pytest.fixture
def countdownPeriod():
    return 600

@pytest.fixture
def threshold():
    return 1000000000000000000

@pytest.fixture
def contribution(project, receiver, owner, countdownPeriod, threshold):
    return owner.deploy(project.Contribution, countdownPeriod, threshold, receiver)

@pytest.fixture
def coordinator_provider_uri():
    return "tester://pyevm"

@pytest.fixture
def coordinator_network():
    return "lynx"
    
@pytest.fixture
def ritual_id():
    return 0

@pytest.fixture
def contract_address(contribution):
    return contribution.address

@pytest.fixture
def encrypt(coordinator_provider_uri, coordinator_network, contract_address):
    print(_CONDITION_CHAINS)

    plaintext = b"paz al amanecer"
    THIS_IS_NOT_A_TRINKET = 2  # sometimes called "public key"

    enrico = _Enrico(encrypting_key=THIS_IS_NOT_A_TRINKET)
    bob = _Bob(domain=coordinator_network, eth_provider_uri=coordinator_provider_uri)

    ANYTHING_CAN_BE_PASSED_AS_RITUAL_ID = 55

    before_the_beginning_of_time = {
        "version": ConditionLingo.VERSION,
        "condition": {
            "chain": 131277322940537,
            "method": "isReleased",
            "contractAddress": contract_address,
            "returnValueTest": {"comparator": "==", "value": True},
            "functionAbi": {"inputs":[],"name":"isReleased","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}
        },
    }

    print(_CONDITION_CHAINS)
    ciphertext, tdr = enrico.encrypt_for_dkg_and_produce_decryption_request(
        plaintext=plaintext,
        conditions=before_the_beginning_of_time,
        ritual_id=ANYTHING_CAN_BE_PASSED_AS_RITUAL_ID,
    )
