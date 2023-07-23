from typing import TypedDict

from nucypher.policy.conditions.lingo import Lingo


class TMK(TypedDict):
    bulk_ciphertext: str  # encoded as base64
    encrypted_sym_key: str  # encoded as hex
    conditions: Lingo
    filename: str
