from Crypto.Hash import SHA256


def key_derivation(passphrase: str) -> bytes:
    """Derive a key from a passphrase.

    `passphrase` is the passphrase to derive the key from.
    """
    sha256 = SHA256.new()
    sha256.update(passphrase.encode('utf-8'))
    return sha256.digest()


class CustomEncryptionMethod:
    def encrypt(self, data, key):
        key_bytes = key_derivation(key)
        return key_bytes + data

    def decrypt(self, data, key):
        key_bytes = key_derivation(key)
        return data[len(key_bytes):]


class SecondEncryptionMethod:
    def encrypt(self, data, key):
        key_bytes = key_derivation(key)
        return key_bytes + data

    def decrypt(self, data, key):
        key_bytes = key_derivation(key)
        return data[len(key_bytes):]
