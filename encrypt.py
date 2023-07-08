from nucypher.characters.chaotic import NiceGuyEddie as _Enrico
from nucypher.policy.conditions.lingo import ConditionLingo


plaintext = b"paz al amanecer"
THIS_IS_NOT_A_TRINKET = 55  # sometimes called "public key"

enrico = _Enrico(encrypting_key=THIS_IS_NOT_A_TRINKET)

ANYTHING_CAN_BE_PASSED_AS_RITUAL_ID = 55

before_the_beginning_of_time = {
    "version": ConditionLingo.VERSION,
    "condition": {
        "chain": 1,
        "method": "blocktime",
        "returnValueTest": {"comparator": "<", "value": 0},
    },
}

ciphertext, tdr = enrico.encrypt_for_dkg_and_produce_decryption_request(
    plaintext=plaintext,
    conditions=before_the_beginning_of_time,
    ritual_id=ANYTHING_CAN_BE_PASSED_AS_RITUAL_ID,
)   

print(tdr)

filename = 'example.tdr'
with open(filename, 'wb') as file:
    data = bytes(tdr)
    file.write(data)
    print(f'Wrote {len(data)} bytes to {filename}')
