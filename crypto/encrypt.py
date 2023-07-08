from cryptography.fernet import Fernet
from eth_utils import keccak


def keygen():
    _secret = Fernet.generate_key()
    return _secret


def encrypt(_secret):
    f = Fernet(_secret)
    secret_hash = keccak(_secret)
    secret_ciphertext = f.encrypt(b"A really secret message.")
    return secret_hash, secret_ciphertext


_secret = keygen()
secret_hash, secret_ciphertext = encrypt(_secret)

print(f"secret: {_secret.hex()}")
print(f"secret hash: {secret_hash.hex()}")
print(f"secret ciphertext: {secret_ciphertext.hex()}")
