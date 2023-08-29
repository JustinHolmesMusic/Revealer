from dataclasses import asdict, dataclass
from typing import Any, NewType, cast

import msgpack
from cryptography.fernet import Fernet
from nucypher.policy.conditions.lingo import Lingo

ClearText = NewType("ClearText", bytes)
BulkCipherText = NewType("BulkCipherText", bytes)


@dataclass
class FilePlaintext:
    file_content: bytes
    metadata: dict[str, Any]

    def to_bytes(self) -> ClearText:
        # Serialize the dictionary to bytes using MessagePack
        data_dict = asdict(self)
        serialized_data: ClearText = msgpack.packb(data_dict)  # type: ignore
        return serialized_data

    @classmethod
    def from_bytes(cls, serialized_data: ClearText) -> "FilePlaintext":
        # Deserialize the bytes to a dictionary using MessagePack
        data_dict: dict[str, Any] = msgpack.unpackb(serialized_data)
        return cls(**data_dict)


def decrypt(ciphertext: BulkCipherText, plaintext_of_symkey: bytes) -> ClearText:
    f = Fernet(plaintext_of_symkey)
    cleartext: ClearText = cast(ClearText, f.decrypt(ciphertext))
    return cleartext


def encapsulate(plaintext_of_symkey: bytes, cleartext: ClearText) -> BulkCipherText:
    f = Fernet(plaintext_of_symkey)
    capsule = cast(BulkCipherText, f.encrypt(cleartext))
    return capsule


@dataclass
class TMK:
    bulk_ciphertext: BulkCipherText
    encrypted_sym_key: bytes
    conditions: Lingo

    def __init__(
        self, bulk_ciphertext: BulkCipherText, encrypted_sym_key: bytes, conditions: Lingo
    ) -> None:
        self.bulk_ciphertext = bulk_ciphertext
        self.encrypted_sym_key = encrypted_sym_key
        self.conditions = conditions

    def to_bytes(self) -> bytes:
        return msgpack.packb(asdict(self))  # type: ignore

    @classmethod
    def from_bytes(cls, serialized_data: bytes) -> "TMK":
        return cls(**msgpack.unpackb(serialized_data))
