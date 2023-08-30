import pytest
from nucypher.characters.chaotic import NiceGuyEddie as _Enrico
from nucypher.policy.conditions.evm import _CONDITION_CHAINS
from nucypher.policy.conditions.lingo import ConditionLingo
from web3 import Web3


@pytest.fixture
def owner(accounts):
    return accounts[0]


@pytest.fixture
def beneficiary(accounts):
    return accounts[1]


@pytest.fixture
def not_owner(accounts):
    return accounts[2]


@pytest.fixture
def amb(accounts):
    return accounts[3]


@pytest.fixture
def countdownPeriod():
    return 600


@pytest.fixture
def threshold():
    return Web3.to_wei(1, "ether")


@pytest.fixture
def contribution(project, beneficiary, owner, countdownPeriod, threshold, amb):
    return owner.deploy(
        project.Contribution,  # contract name
        countdownPeriod,  # countdown period
        threshold,  # threshold
        Web3.to_wei(0.1, "ether"),  # min contribution
        60 * 60 * 24 * 14,  # initial window (14 days)
        beneficiary,
        False,  # testnet mode
    )


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
def dummy_key_base64():
    return b"6G4O0AusEgrJ_maWYYiM5i_S1OtznIYcjRsehJjplEM="


@pytest.fixture
def dummy_key_ciphertext_base64():
    return b"gAAAAABkqYAnoyOibrOGDpql3D58PQn_UXw9o-xCPtEF1sxEHMc8TknAcJMqO2MCzWDsVD5TJ9AhYGZmnfVLYGavp7ch_BdZmR9sAIsYUUUNDRQGK-7tlXI="


@pytest.fixture
def dummy_key_hash():
    return b'HKu\xef\xd8\xcb\x81\x0fW\x13\xc1\xd3B\x0c\x0c\xe1\xa3"w\x16I\xe1\x1a\x92l\xc4\xe4^\xffz\x80\x00'


@pytest.fixture
def encrypt(coordinator_provider_uri, coordinator_network, contract_address):
    print(_CONDITION_CHAINS)

    plaintext = b"paz al amanecer"
    THIS_IS_NOT_A_TRINKET = 2  # sometimes called "public key"

    enrico = _Enrico(encrypting_key=THIS_IS_NOT_A_TRINKET)
    # bob = _Bob(domain=coordinator_network, eth_provider_uri=coordinator_provider_uri)

    ANYTHING_CAN_BE_PASSED_AS_RITUAL_ID = 55

    before_the_beginning_of_time = {
        "version": ConditionLingo.VERSION,
        "condition": {
            "chain": 131277322940537,
            "method": "isReleased",
            "contractAddress": contract_address,
            "returnValueTest": {"comparator": "==", "value": True},
            "functionAbi": {
                "inputs": [],
                "name": "isReleased",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            },
        },
    }

    print(_CONDITION_CHAINS)
    ciphertext, tdr = enrico.encrypt_for_dkg_and_produce_decryption_request(
        plaintext=plaintext,
        conditions=before_the_beginning_of_time,
        ritual_id=ANYTHING_CAN_BE_PASSED_AS_RITUAL_ID,
    )


TESTERCHAIN_CHAIN_ID = 131277322940537


@pytest.fixture(scope="session", autouse=True)
def mock_condition_blockchains(session_mocker):
    """adds testerchain's chain ID to permitted conditional chains"""
    session_mocker.patch.dict(
        "nucypher.policy.conditions.evm._CONDITION_CHAINS",
        {TESTERCHAIN_CHAIN_ID: "eth-tester/pyevm"},
    )
